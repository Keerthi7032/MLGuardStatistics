import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from IPython.display import display, HTML
import MySQLdb
import pandas as pd
import datetime as dt
from collections import OrderedDict


def get_for(st,df,uni_cid):
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
    conn = MySQLdb.connect(host="107.180.71.58",
                  port=3306,
                  user="root",
                  passwd="root",
                  db="mlcharts")
    cur=conn.cursor()
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
    return div