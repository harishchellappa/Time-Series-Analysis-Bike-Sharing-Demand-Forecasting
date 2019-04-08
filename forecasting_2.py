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




df = pd.read_excel('newtable.xlsx',sheet_name='newtable')

df.head()
df.dtypes



df['start_time']=pd.to_datetime(df['start_time'],format="%d/%m/%Y %I:%M:%S %p")
df['end_time']=pd.to_datetime(df['end_time'],format="%d/%m/%Y %I:%M:%S %p")  
  

# df['end_time'].head(10)


df_d = pd.pivot_table(df[['start_station','start_time']],aggfunc='count',index=df['start_time'].dt.date,columns=['start_station'],fill_value=0)  #date


 #working on code for removing inactive stations

ial=[('start_time',3021),	('start_time',3053),	('start_time',3055),	('start_time',3059),	
     ('start_time',3060),	('start_time',3061),	('start_time',3079),	('start_time',3080),	
     ('start_time',4108),	('start_time',4138),	('start_time',4142),	('start_time',4143),	
     ('start_time',4144),	('start_time',4146),	('start_time',4147),	('start_time',4148),	
     ('start_time',4149),	('start_time',4150),	('start_time',4151),	('start_time',4152),	
     ('start_time',4153),	('start_time',4154),	('start_time',4155),	('start_time',4156),	
     ('start_time',4157),	('start_time',4158),	('start_time',4159),	('start_time',4160),	
     ('start_time',4162),	('start_time',4163),	('start_time',4165),	('start_time',4166),	
     ('start_time',4167),	('start_time',4169),	('start_time',4170),	('start_time',4174),	
     ('start_time',4176),	('start_time',4177),	('start_time',4180),	('start_time',4181),	
     ('start_time',4183),	('start_time',4194),	('start_time',4244),
     ('start_time',4276)] # 44 stations removed 43 start stations are inactive right now + 3 bakchods stations (4110,4118,4276) which had station table rows blank, 4110 4118 not in start_station

df_d.drop(labels=ial,axis=1,inplace=True)


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

with pd.ExcelWriter('outputY.xlsx') as writer:  # doctest: +SKIP
    df_d.to_excel(writer,sheet_name='actual(Y)')
    df_o.to_excel(writer,sheet_name='predicted(Y)')
    mse_trn.to_excel(writer,sheet_name='mse_trn(Y)')
    mse_tst.to_excel(writer,sheet_name='mse_tst(Y)')



# mean mse value for 


 ''' 
df_o.tail()
tst.tail()

df_o.loc[df_o.index[int(0.8*len(df_o.index)):]].plot(x='ds',y=v)

tst.plot(x='ds',y='y')

y_actual=tst['y']
y_predicted=df_o[v][df_o.index[int(0.8*len(df_o.index)):]]

mse = sqrt(mean_squared_error(y_actual, y_predicted))
print(mse)
'''
'''
mse with weekly 11.685
mse without weekly 13.04
'''
#df_m=pd.pivot_table(df[['start_station','start_time']],aggfunc='count',index=[df['start_time'].dt.year,df['start_time'].dt.month],columns=['start_station'],fill_value=0)   #month year
#df_d=pd.pivot_table(df[['start_station','start_time']],aggfunc='count',index=df['start_time'].dt.date,columns=['start_station'],fill_value=0)
#df_d['index']=df_d.index    # converting index to a row in data frame



dft1=pd.DataFrame(list(df_d['index']),columns=['ds'])
dft1.rename(columns={'0':'ds'}, inplace=True)
dft1['y']=list(df_d.iloc[:,0])
dft1.head()

dft2=dft1.iloc[0:-25,:]
dft2.tail()
dftv=dft1.iloc[-25:,:]
dftv.head()
dft2.plot(x='ds',y='y')
dftv.plot(x='ds',y='y')


m=Prophet()
m.fit(dft2)

future = m.make_future_dataframe(periods=25)
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()





###############################################################################

#month analysis
df_m['index']=df_m.index
dft1 = pd.DataFrame(list(df_m['index']))#,columns=['ds'])
#dft1.rename(columns={'0':'year','1':'month'}, inplace=True)

dft1['y']=list(df_m.iloc[:,0])
dft1.head()

df_m.columns[0]
df_m.plot(x='index',y=df_m.columns[0])

dft2=dft1.iloc[0:-25,:]
dft2.tail()
dftv=dft1.iloc[-25:,:]
dftv.head()
dft2.plot(x='ds',y='y')
dftv.plot(x='ds',y='y')


m=Prophet()
m.fit(dft2)

future = m.make_future_dataframe(periods=25)
forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

fig1 = m.plot(forecast)

