# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 17:25:47 2019

@author: mayank
"""

import pandas as pd
import numpy as np
from fbprophet import Prophet
from datetime import datetime
from sklearn.model_selection import train_test_split
from matplotlib import pyplot 

from sklearn.metrics import mean_squared_error
from math import sqrt




df = pd.read_excel('C:/Users/tusha/Desktop/newtable.xlsx',sheet_name='newtable')

df.head()
df.dtypes



df['start_time']=pd.to_datetime(df['start_time'],format="%d/%m/%Y %I:%M:%S %p")
df['end_time']=pd.to_datetime(df['end_time'],format="%d/%m/%Y %I:%M:%S %p")  

#calculating the revenue from each trip not tsking the membership fees into consideration
def revenue(passtype,duration,time):
   perthirty=1.75
   if(time<date(year=2018,month=7,day=12)):
      perthirty=3.5 
   cost=0
   qty=int(duration/30)
   extra=duration %30
   if(extra!=0):
      qty=qty+1
   if(passtype== 'Monthly Pass' or passtype== 'Annual Pass' or passtype == 'One Day Pass' or passtype == 'Flex Pass'):
      qty=qty-1
   if(qty<0):
      qty=0
   cost=perthirty*qty
   return cost

rev=list()
for passtype,duration,time in zip(df['passholder_type'],df['trip_duration'],df['start_time']):
    rev.append(revenue(passtype,duration,time.date()))

df['revenue']=rev   

 

# df['end_time'].head(10)


df_d = pd.pivot_table(df[['revenue','start_time']],aggfunc='sum',index=df['start_time'].dt.date,fill_value=0)  #date


df_d.index = pd.to_datetime(df_d.index)
         

## imported from the cycling event url:https://www.ciclavia.org/events_history
#rem=['2016-08-14','2018-10-16','2017-03-26','2017-05-11','2017-08-13','2017-10-08',\
#           '2017-12-10','2018-04-22','2018-06-24','2018-09-30','2018-12-02']
#
#df_d['temp']=df_d.index   # creating a column of indexes
#
#for l in rem:
#    df_d=df_d[df_d.temp!=l]            # removing the rows with rem values as these are the outliers
#    
#
#df_d.drop('temp',axis=1,inplace=True)  # removing the index column



df_o=pd.DataFrame()
mse_trn=[]
mse_tst=[]

for i,v in enumerate(df_d.columns):
    #i=0
    #v=('start_time', 3005)
    
    def prophet_inputize(df,column_num = 0):
        df_1 = pd.DataFrame()
        df_1['ds'] = df.index
        df_1['y'] = list(df.iloc[:,i])
        return(df_1)
    
    def do_something(df_d,sample ='D',test =-184):
        
        
        #df_d = df_d.resample(sample).sum()
        
        # imported from the cycling event url:https://www.ciclavia.org/events_history
        rem=['2016-08-14','2018-10-16','2017-03-26','2017-05-11','2017-08-13','2017-10-08',\
           '2017-12-10','2018-04-22','2018-06-24','2018-09-30','2018-12-02']

        df_d['temp']=df_d.index   # creating a column of indexes

        for l in rem:
            df_d=df_d[df_d.temp!=l]            # removing the rows with rem values as these are the outliers
    

        df_d.drop('temp',axis=1,inplace=True)  # removing the index column
        
        
        df_d_trn = pd.DataFrame()
        df_d_tst = pd.DataFrame()
        
        df_d_trn = df_d.loc[df_d.index[:test]]#int(train_prop*len(df_d.index))]]
                
        df_d_tst = df_d.loc[df_d.index[test:]]#int(train_prop*len(df_d.index)):]]
    
        df_d_trn = prophet_inputize(df_d_trn,i)
        df_d_tst = prophet_inputize(df_d_tst,i)
    
#        df_d_trn.plot(x='ds',y='y')
#        df_d_tst.plot(x='ds',y='y')
        
        return(df_d_trn,df_d_tst)

    
    sample_freq = 'D'
    trn, tst = do_something(df_d,sample_freq,-184)    
    m = Prophet(yearly_seasonality=True,weekly_seasonality= False,daily_seasonality=False)
    m.fit(trn)
    future = m.make_future_dataframe(periods=len(tst)+90+3,freq=sample_freq)    # till 31st march 2019 q1 2019
    forecast = m.predict(future)
    df_o[v]=forecast['yhat']
#    df_o['ds']=forecast['ds']
#    fig1 = m.plot(forecast)
#    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
#    print(tst.tail())
    y_actual_tst=tst['y']
    y_predicted_tst=df_o[v][df_o.index[-184:]]
    mse_tst.append(sqrt(mean_squared_error(y_actual_tst, y_predicted_tst)))
    
    y_actual_trn=trn['y']
    y_predicted_trn=df_o[v][df_o.index[:-184-93]]                              ## removing q1 2019 dates
    mse_trn.append(sqrt(mean_squared_error(y_actual_trn, y_predicted_trn)))

df_o['ds']=forecast['ds']



### now run this


# imported from the cycling event url:https://www.ciclavia.org/events_history
rem=['2016-08-14','2018-10-16','2017-03-26','2017-05-11','2017-08-13','2017-10-08',\
           '2017-12-10','2018-04-22','2018-06-24','2018-09-30','2018-12-02']

df_d['ds']=df_d.index   # creating a column of indexes

for l in rem:
    df_d=df_d[df_d.ds!=l]            # removing the rows with rem values as these are the outliers
    
df_d=df_d.reset_index(drop=True)     # reset index to zero

mse_trn=pd.DataFrame(mse_trn)
mse_tst=pd.DataFrame(mse_tst)


#import statistics
#import math
#statistics.mean(mse)   

with pd.ExcelWriter('outputY_Revenue.xlsx') as writer:  # doctest: +SKIP
    df_d.to_excel(writer,sheet_name='actual(Y)')
    df_o.to_excel(writer,sheet_name='predicted(Y)')
    mse_trn.to_excel(writer,sheet_name='mse_trn(Y)')
    mse_tst.to_excel(writer,sheet_name='mse_tst(Y)')
