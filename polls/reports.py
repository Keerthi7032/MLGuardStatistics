import pandas as pd
import MySQLdb
from datetime import datetime
import calendar
from collections import OrderedDict
import base64
from io import BytesIO
from PIL import Image
import plotly.offline as py
import plotly.graph_objs as go


def get_for(st,df):
    company={}
    query = "SELECT cid, name FROM company"
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for i in range(len(rows)):
        company[rows[i][0]] = rows[i][1]
    uni_cid = list(company.keys())
    lis=list(company.values())
    lis=[st]+lis
    grouped=df.groupby([st,'cid'])
    statis = get_statistics(df,company,uni_cid,grouped)
    return statis

def get_statistics(df,company,uni_cid,grouped):
    inter_lis=[]
    dic2={}
    for name, group in grouped:
        #print(name)
        #print(group['cid'].count())
        if(name[0] in dic2.keys()):
            dic2[name[0]][company[name[1]]]=group['cid'].count()
        else:
            dic2[name[0]]=dict(zip(list(company.values()),[0]*len(uni_cid)))
            dic2[name[0]][company[name[1]]]=group['cid'].count()
    # print(dic2)
    dic3={}
    for i in dic2.keys():
        dictlist=[]
        for key, value in dic2[i].items():
            temp = [key,value]
            dictlist.append(temp)
        temp_date = i
        dic3[str(temp_date)]=dictlist
        # print(str(i))
    # print(dic2)
    return dic3

def get():
    div=[]
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    df=pd.read_sql("Select in_time,cid from faces_log",conn)
    df['year'] = df['in_time'].dt.year
    df['month'] = df['in_time'].dt.month.apply(lambda x: calendar.month_name[x])
    df['day'] = df['in_time'].dt.day
    df['time'] = df['in_time'].dt.hour
    df['date'] = df['in_time'].dt.date
    df.drop('in_time',axis=1,inplace=True)
    l=['year','month','day','time','date']
    df1=get_for('year',df)
    df2=get_for('month',df)
    df3=get_for('date',df)
    df4=get_for('time',df)
    div.append(df1)
    div.append(df2)
    div.append(df3)
    div.append(df4)

    # get uptime of all MLGuards
    query = "SELECT name, last_uptime FROM uptime"
    uptime_df = pd.read_sql(query, conn)
    div.append(uptime_df.to_html())

    # get downtime of all MLGuards
    div.append(check_status())
    div.append(check_camera_status())
    return div


def check_status():
    uptimes_all = {}
    company = {}
    status_df = pd.DataFrame()
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur_time = datetime.strptime(cur_time, '%Y-%m-%d %H:%M:%S')

    query = "SELECT cid, name FROM company"
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    for i in range(len(rows)):
        company[rows[i][0]] = rows[i][1]

    query = "SELECT cid, last_uptime FROM uptime"
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    for i in range(len(rows)):
        uptimes_all[rows[i][0]] = rows[i][1]

    for cid, uptime in uptimes_all.items():

        l=[]
        if uptime == None:
            uptime = datetime.strptime('2018-03-15 00:00:00', '%Y-%m-%d %H:%M:%S')
        diff_time = cur_time - uptime

        if (diff_time.seconds > 3900):
            l.append(company[cid])
            l.append("The MLGuard is down !!")
            l.append(diff_time)
            df2 = pd.DataFrame([l],columns=['Device Name', 'Status', 'Down Time Duration'])
        else:
            l.append(company[cid])
            l.append("The MLGuard is up !!")
            l.append("00:00:00")
            df2 = pd.DataFrame([l],columns=['Device Name', 'Status', 'Down Time Duration'])
        status_df=status_df.append(df2, ignore_index=True)
    return status_df.to_html()


# --------------------    Displaying Images ------------------------------


username = "root"
pwd = "root"
dbname = "mlcharts"
port = 3306
host = "107.180.71.58"

def get_connection():
    #connection establishment
    conn = MySQLdb.connect(host=host, user=username, password=pwd, db=dbname)
    return conn

def get_cid(email):
    conn = get_connection()
    cur = conn.cursor()
    query = "select cid from mlguard_admin where email='" + str(email) + "'"
    cur.execute(query)
    print(query)
    t = cur.fetchall()
    cid = t[0][0]
    return cid

def run_query(query):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query)
    f = cur.fetchall()
    return f[0][0]

# def get_min_max_date(cid):
#     query = "SELECT min(in_time) FROM cars_log where cid=" + str(cid)
#     f = run_query(query)
#     query = "SELECT max(in_time) FROM cars_log where cid=" + str(cid)
#     t = run_query(query)
#     return (f, t)

def get_data(cid):
    conn = get_connection()
    cur = conn.cursor()
    query = "select id, in_time, face_image from faces_log where cid=" + str(cid)
    cur.execute(query)
    t = cur.fetchall()

    b = [list(x) for x in t]
    for i in range(len(b)):
        file_like = BytesIO(b[i][2])
        img = Image.open(file_like)
        img.save("retrieved_image.jpg")

        image_file = "retrieved_image.jpg"
        with open("retrieved_image.jpg", "rb") as image_file:
            img_encoded = base64.b64encode(image_file.read())

        b[i][2] = img_encoded
    return b

def get_hist_plot(df, key):
    # print(df)
    x = df[key]
    # print(x)
    xaxis = dict(title='Years', titlefont=dict(family='sans serif', size=18, color='#7f7f7f'))
    yaxis = dict(title='Count', titlefont=dict(family='sans serif', size=18, color='#7f7f7f'))
    data = [go.Bar(y=[x[i][1] for i in range(len(x))], x=[x[i][0] for i in range(len(x))])]
    layout = go.Layout(title="MLGuard Users Summary", xaxis=xaxis, yaxis=yaxis, height=500, width=1200)
    figure = go.Figure(data=data, layout=layout)
    return py.plot(figure,auto_open = True, output_type = 'div')

    # data = [go.Bar(
    #     x=['giraffes', 'orangutans', 'monkeys'],
    #     y=[20, 14, 23]
    # )]
    #
    # py.iplot(data, filename='basic-bar')

def gen_charts(df,key):
    l = []
    div = get_hist_plot(df,key)
    l.append(div)
    return l

def get_users():
    conn = get_connection()
    cur = conn.cursor()
    query = "select name from company"
    cur.execute(query)
    t = cur.fetchall()
    users = [t[i][0] for i in range(len(t))]
    return users

# def get_chart_data(selected_user):
#     # get cid of the selected user
#     if(selected_user == "All"):
#         where_clause = ""
#     else:
#         where_clause = " where name="+str(selected_user)
#
#     conn = get_connection()
#     cur = conn.cursor()
#     query = "select cid from company where name=" + str(selected_user)
#     cur.execute(query)
#     t = cur.fetchall()
#     cid = [t[i][0] for i in range(len(t))]

def get_df_data():
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    df = pd.read_sql("Select in_time,cid from faces_log", conn)
    df['year'] = df['in_time'].dt.year
    df['month'] = df['in_time'].dt.month.apply(lambda x: calendar.month_name[x])
    df['day'] = df['in_time'].dt.day
    df['time'] = df['in_time'].dt.hour
    df['date'] = df['in_time'].dt.date
    df.drop('in_time', axis=1, inplace=True)
    return df

def get_chart_data(selected_option):
    df = get_df_data()
    l = ['year', 'month', 'day', 'time', 'date']
    df1 = get_for('year', df)
    key=""
    data={}

    if(selected_option['day'] == 'All' and selected_option['month'] == 'All'):
        data = df1
        key = selected_option['year']
    elif(selected_option['day'] == 'All'):
        year_df = df[df['year'] == int(selected_option['year'])]
        month_df = get_for('month', year_df)
        data = month_df
        key = selected_option['month']
    else:
        year_df = df[df['year'] == int(selected_option['year'])]
        month_df = year_df[year_df['month'] == selected_option['month']]
        df2 = get_for('day', month_df)
        data = df2
        key = selected_option['day']

    return gen_charts(data, key)

def get_years():
    df = get_df_data()
    dic = {"years": df['year'].unique()}
    return dic

def get_months():
    df = get_df_data()
    lis = list(df['month'].unique())
    months = {"months":lis}
    return months

def get_days():
    df = get_df_data()
    year_df = df[df['year'] == 2018]
    month_lis = year_df['month'].unique()
    dict = {}
    for i in month_lis:
        month_df = year_df[year_df['month'] == i]
        dict[i] =list(month_df['day'].unique())
    days = dict
    print(days)
    return days

# --------------------    Check camera status   ------------------------------

def check_camera_status():
    query = "SELECT cid, status FROM check_camera"
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    df = pd.read_sql(query, conn)
    return df.to_html()