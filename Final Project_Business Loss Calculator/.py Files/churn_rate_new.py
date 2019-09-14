# -*- coding: utf-8 -*-
"""Churn_Rate_New.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pW0V-TmmiSWMN7wHQ1G6bXXI8aNat2ih
"""

import pandas_redshift as pr
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from statsmodels.tsa.arima_model import ARIMA

db_name = "info7374dbassignment2"#-------------------------------------Redshift: Database Name for gaming data

master_username = ""#----------------------------------------Redshift: Admin Username
master_password = ""#---------------------------------Redshift: Admin Password


hostname = "info7374clusterproject.cwtvmzfhaqaf.us-east-1.redshift.amazonaws.com" #----------------Redshift: Hostname for database
port_number = 5439    #----------------Redshift: Port Number for databse

pr.connect_to_redshift(dbname = db_name ,
                        host = hostname,
                        port = port_number,
                        user = master_username,
                        password =master_password)

online = pr.redshift_to_pandas('select * from sales')

online.head(5)

# drop the row missing customerID
online = online[online.customerid.notnull()]

# extract year, month and day 
online['invoiceday'] = online.invoicedate.apply(lambda x: dt.datetime(x.year, x.month, x.day))
online.head()

monthly_unique_customers_df = online.set_index('invoiceday')['customerid'].resample('M').nunique()

monthly_unique_customers_df

pd.DataFrame(monthly_unique_customers_df)['invoicedate']=pd.DataFrame(monthly_unique_customers_df).index

df = pd.DataFrame(monthly_unique_customers_df).reset_index()
df["CustomerIDshift"] = [0]+list(df["customerid"][:-1])
df["ChurnRate"] = (df["CustomerIDshift"]-df["customerid"])/df["CustomerIDshift"]
df.rename(columns={'invoiceday': 'Month'}, inplace=True)
df['ChurnRate'][0]=1
df['ChurnRate']

data = df.drop(columns=['customerid','CustomerIDshift'])

