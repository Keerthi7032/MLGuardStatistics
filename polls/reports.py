import pandas as pd
import MySQLdb
from datetime import datetime
from collections import OrderedDict


def get_for(st,df,uni_cid):
    # company = {}
    # query = "SELECT cid, name FROM company"
    # conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    # cur = conn.cursor()
    # cur.execute(query)
    # rows = cur.fetchall()
    # for i in range(len(rows)):
    #     company[rows[i][0]] = rows[i][1]

    lis=[st,'Office','Banglore','Keerthi','Ravi','Alekhya','Goutham','Device8','Device9','Siri','Manoj']
    grouped=df.groupby([st,'cid'])
    year_statis = get_statistics(df,lis,uni_cid,grouped)
    df_year=pd.DataFrame(columns=lis)
    ldf=[]
    j=0
    for i in year_statis.keys():
        
        ldf=[i]+list(OrderedDict(sorted(year_statis[i].items())).values())
        df_year.loc[j] = ldf
        j=j+1
    return df_year

def get_statistics(df,lis,uni_cid,grouped):
    inter_lis=[]
    dic=dict(zip(uni_cid,[0]*len(uni_cid)))
    dic2={}
    for name,group in grouped:
        #print(name)
        #print(group['cid'].count())
        if(name[0] in dic2.keys()):
            dic2[name[0]][name[1]]=group['cid'].count()
        else:
            dic2[name[0]]=dict(zip(uni_cid,[0]*len(uni_cid)))
            dic2[name[0]][name[1]]=group['cid'].count()
        #print(dic2)
    return dic2

def get():
    div=[]
    conn = MySQLdb.connect(host="107.180.71.58", port=3306, user="root", passwd="root", db="mlcharts")
    df=pd.read_sql("Select in_time,cid from faces_log",conn)
    df['year'] = df['in_time'].dt.year
    df['month'] = df['in_time'].dt.month
    df['day'] = df['in_time'].dt.day
    df['time'] = df['in_time'].dt.hour
    df['date'] = df['in_time'].dt.date
    df.drop('in_time',axis=1,inplace=True)
    uni_cid = list(df['cid'].unique())
    l=['year','month','day','time','date']
    df1=get_for('year',df,uni_cid)
    df2=get_for('month',df,uni_cid)
    df3=get_for('day',df,uni_cid)
    df4=get_for('date',df,uni_cid)
    div.append(df1.to_html())
    div.append(df2.to_html())
    div.append(df3.to_html())
    div.append(df4.to_html())

    # get uptime of all MLGuards
    query = "SELECT cid, last_uptime FROM uptime"
    uptime_df = pd.read_sql(query, conn)
    div.append(uptime_df.to_html())

    # get downtime of all MLGuards
    div.append(check_status())
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