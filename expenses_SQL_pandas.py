import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import datetime as dt
import numpy as np
import os

#how to connect to database via psycopg2


#connect to database via "sqlalchemy" for reading and writing from/to database
engine=create_engine(os.environ.get("ENGINE_SQLALCHEMY"))

class Finansial_df():

    transactions=pd.read_sql('transactions',engine,index_col="id")
    accounts=pd.read_sql('accounts',engine,index_col="id")

    def __init__(self,engine):
        self.engine=engine

    def weekly_analysis(self):
        week_df=self.transactions.loc[pd.to_datetime(self.transactions["date"])>=dt.datetime.today()-pd.offsets.Week(weekday=6)]
        week_df=week_df.loc[(week_df['merchant_name']!="None")&(week_df['merchant_name']!='Broadmoor Ridge')]
        week_df=week_df.sort_values('date')
        week_sum=week_df.loc[week_df["amount"].astype(float)>0]["amount"].astype(float).sum()
        week_mean=round(week_df.loc[week_df["amount"].astype(float)>0]["amount"].astype(float).mean(),2)
        return f"total spending for the week: ${week_sum}\nmean amount: ${week_mean}"
    def monthly_analysis(self):
        month_df=self.transactions.loc[pd.to_datetime(self.transactions["date"])>=dt.datetime.today()-pd.offsets.MonthEnd()]
        month_df=month_df.loc[month_df['merchant_name']!="None"]
        month_df=month_df.sort_values('date')
        month_sum=round(month_df.loc[month_df["amount"].astype(float)>0]["amount"].astype(float).sum(),2)
        month_mean=round(month_df.loc[month_df["amount"].astype(float)>0]["amount"].astype(float).mean(),2)
        return f"total spending for the month: ${month_sum}\nmean amount: ${month_mean}"
    def weekly_transactions(self):
        week_df=self.transactions.loc[pd.to_datetime(self.transactions["date"])>=dt.datetime.today()-pd.offsets.Week(weekday=6)]
        week_df.loc[week_df.merchant_name=="None",'merchant_name']=week_df.name
        week_df=week_df.sort_values('date',ascending=False)
        week_df=week_df[["merchant_name","amount"]]
        week_df=week_df.set_index('merchant_name')
        return week_df
    def current_fin_state(self):
        self.accounts.amount=(self.accounts.limit_amount-self.accounts.amount)*(-1)
        return f"yor total amount is ${round(self.accounts.amount.sum())}"

df=Finansial_df(engine)





