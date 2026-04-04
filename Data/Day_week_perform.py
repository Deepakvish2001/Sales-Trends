from feature_engineer import *


# Average revenue/transaction by day of week
def get_weekly_revenue(df):
    return(df.groupby('weekday').agg(
    revenue = ('revenue','mean'),
    transaction_qty = ('transaction_qty','count')).reindex(week_order).reset_index())
    # avg_revenue.rename(columns={'revenue': 'avg_revenue'}, inplace=True)


# # Average transaction count by day
# daily = df.groupby('weekday')['transaction_qty'].count().reset_index()
# avg_transaction = daily.groupby('weekday')['transaction_id'].mean().reindex(week_order).reset_index()
# print(f"Average Transaction is \n {avg_transaction}")

#Weekday vs weekend comparison
def get_week_weekend(df):
    df['week'] = df['weekday'].isin(['Saturday','Sunday']).map({True: 'Weekend', False: 'Week'})
    return(df.groupby('week').agg(revenue = ('revenue','sum'),transaction_qty = ('transaction_qty','count')).reset_index())
# print(f"week comaprison \n  {week_comparison}")

def interpret_behaviour(df):
    df['day_type'] = df['weekday'].isin(['Saturday','Sunday']).map({True: 'Weekend', False: 'Weekday'})
    summary = df.groupby('day_type').agg(revenue = ('revenue','sum'), transaction_id = ('transaction_id','count'),avg_order_value=('revenue','mean')).reset_index()
    weekday = summary[summary['day_type']=='Weekday'].iloc[0]
    weekend = summary[summary['day_type']=='Weekend'].iloc[0]
    insights = []
    # if 'Weekday' not in summary['day_type'].values or 'Weekend' not in summary['day_type'].values:
    #     insight.append("Not enough data to compare Weekday vs Weekend")
    #     return insight
    if weekend['revenue'] > weekday['revenue']:
        insights.append("Revenue -> Weekend has higher revenue -> leisure day")
    else:
        insights.append("Revenue -> Weekday has high revenue -> workday")
    if weekend['transaction_id'] > weekday['transaction_id']:
        insights.append("Transaction id -> Customer spend more per order -> weekend")
    else:
        insights.append("Transaction id -> Weeker Transaction is higher -> workday")

    return insights

print(df.info())