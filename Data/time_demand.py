from feature_engineer import *

# Time-of-Day Demand Analysis
# • Hourly transaction volume curves
def get_hours_analysis(df):
    return(df.groupby('hour').agg(
        revenue = ('revenue','sum'),
        transaction_qty = ('transaction_qty','sum')
    ).reset_index())
# pivottable = hour_transaction.pivot(index='hour',columns='weekday',values='transaction_id')


# • Identification of:
# ○ Morning rush hours
# ○ Midday slow periods
# ○ Evening peaks
def get_peak(df):
    result = {}
    #-------Morning Rush Hour-------
    morning_data = df[df['time_bucket']=='Morning']
    morning_peak = morning_data.groupby('hour').agg(revenue = ('revenue','sum'),transaction_qty = ('transaction_qty','sum'))
    result['morning_revenue_hour'] = morning_peak['revenue'].idxmax()
    result['morning_transaction_hour'] = morning_peak['transaction_qty'].idxmax()

    #-------Midday slow Period------
    midday_data = df[df['time_bucket']=='Afternoon']
    midday_group = midday_data.groupby('hour').agg(revenue = ('revenue','sum'),transaction_qty = ('transaction_qty','sum'))
    result['midday_revenue_hour'] = midday_group['revenue'].idxmin()
    result['midday_transaction_hour'] = midday_group['transaction_qty'].idxmin()


    #-------Evening Peak-------------
    evening_data = df[df['time_bucket']=='Evening']
    evening_group = evening_data.groupby('hour').agg(revenue = ('revenue','sum'),transaction_qty = ('transaction_qty','sum'))
    result['evening_revenue_hour'] = evening_group['revenue'].idxmax()
    result['evening_transaction_hour'] = evening_group['transaction_qty'].idxmax()
    return result


insight = get_peak(df)
print(insight)

