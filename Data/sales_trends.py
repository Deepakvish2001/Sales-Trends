from feature_engineer import *
import pandas as pd
import numpy as np


#sales Trends
#daily revenue trends
def get_daily_trends(df):
    return(df.groupby(df['datetime'].dt.date).agg(
        revenue = ('revenue','sum'),
        transaction_qty =('transaction_qty','sum'))
            .reset_index()
            .rename(columns={'datetime':'date'}))

# weekly_trends = df.groupby(pd.Grouper(key='datetime', freq='W'))['revenue'].sum()
# weekly_transaction = df.groupby(pd.Grouper(key='datetime', freq='W'))['transaction_id'].sum()
# print(f"Weekly revenue Trends is \n {weekly_trends}")
# print(f"Weekly revenue Trends is \n {weekly_transaction}")

# Weekly aggregation of revenue and transactions
def get_weekly_Trend(df):
    return(df.groupby(pd.Grouper(key='datetime', freq='W-MON')).agg(
        revenue=('revenue','sum'),transaction_qty =('transaction_qty','sum'))
            .reset_index()
            .rename(columns={'datetime':'date'}))
# print(f"Weekly Trends \n {weekly}")

#montly aggregation of revenue and  transaction
def get_monthly_Trend(df):
    return(df.groupby(pd.Grouper(key='datetime', freq='MS')).agg(
        revenue=('revenue','sum'),transaction_qty =('transaction_qty','sum'))
            .reset_index()
            .rename(columns={'datetime':'date'}))

#  Identification of upward/downward patterns
#weekly pattern
weekly_trend = df.groupby(pd.Grouper(key= 'date',freq='W'))['revenue'].sum().reset_index()
weekly_trend['diff'] = weekly_trend['revenue'].diff()
weekly_trend['trend'] = weekly_trend['diff'].apply(
    lambda x: 'Upward' if x> 0 else ('Downward' if x<0 else 'no change')
)
print(weekly_trend)

#monthly pattern
monthly_trend = df.groupby(pd.Grouper(key='date',freq='M'))['revenue'].sum().reset_index()
monthly_trend['diff'] = monthly_trend['revenue'].diff()
monthly_trend['pattern'] = monthly_trend['diff'].apply(
    lambda x: 'Upward' if x>0 else('Downward' if x<0 else 'No change')
)
print(monthly_trend)

# store-level Trend comparison
def get_store_comparision(df):
    return(df.groupby(['store_location','date']).agg(
    revenue = ('revenue','sum'),
    transaction_qty = ('transaction_qty','sum')).reset_index())
    
# print(f"Trends of store-level comparision \n {store_level}")