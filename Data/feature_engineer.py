import pandas as pd
from load_data_validation import df


# revenue per transaction
df['revenue'] = df['transaction_qty'] * df['unit_price']
# df['hour'] = df['transaction_time'].dt.hour

# Extract Hours
df['hour'] = df['datetime'].dt.hour

# Time Bucket
def time_bucket(hour):
    if 6 <= hour <=11:
        return "Morning"
    elif 12 <= hour <=16:
        return "Afternoon"
    elif 17 <= hour <=21:
        return "Evening"
    else:
        return "Late Night"

df["time_bucket"] = df['hour'].apply(time_bucket)

week_order =  ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
hour_order = [6,7,8,9,10,11,12,13,14,15,16,17,18]
# print(df.head(5))
# print(df.info())
# clean = df.to_excel(r"C:\DV\Sales Trends\update data\cleandata.xlsx",index=False)