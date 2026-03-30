import pandas as pd
import numpy as np
from datetime import datetime

# Load transaction dataset
df = pd.read_excel("C:\DV\Sales Trends\Data\Afficionado Coffee Roasters.xlsx")

# Check for missing or duplicate transaction IDs
# print(df.duplicated().any())
# print(df.isna().any())


# chatgpt
# Sort data (VERY IMPORTANT)
# df = df.sort_values(by='transaction_time').reset_index(drop=True)

# Step 1: Detect day change (when time decreases)
df['new_day'] = df['transaction_time'] < df['transaction_time'].shift(1)

# Step 2: Create day counter
df['day'] = df['new_day'].cumsum()

# Step 3: Create base date using year
df['date'] = pd.to_datetime(df['year'], format='%Y') + pd.to_timedelta(df['day'], unit='D')

df['transaction_time'] = pd.to_datetime(
    df['transaction_time'],
    format='%H:%M:%S',
    errors='coerce'
).dt.time
df['datetime'] = df['date'] + pd.to_timedelta(df['transaction_time'].astype(str))

df['weekday'] = df['date'].dt.day_name()

# Verify logical consistency (positive quantities and prices)
invalid_rows = df[(df['unit_price'])<=0 | (df['transaction_qty']<=0)]
print(f"invalid row is:\n {invalid_rows}")

# df.drop(columns=['day','new_day'],inplace=True)
# print(df.head(20))