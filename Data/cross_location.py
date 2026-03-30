from feature_engineer import *

# Cross-Location Temporal Comparison
# • Hourly heatmaps per store
def get_hourly_heatmap(df):
    return df.groupby(['store_location','hour']).agg(revenue = ('revenue','sum'), transaction_qty = ('transaction_qty','sum')).reset_index()


def customer_insight(df):
    store_insight = []
    if df.empty:
        return store_insight

    for store in df['store_location'].unique():
        
        data = df[df['store_location']== store]

        if data.empty:
            continue
        
        # Time bucket totals (IMPORTANT: sum, not dataframe)
        morning = data[data['time_bucket']=='Morning']['revenue'].sum()
        afternoon = data[data['time_bucket']=='Afternoon']['revenue'].sum()
        evening = data[data['time_bucket']=='Evening']['revenue'].sum()
        
        # Peak hour
        peak_hour = data.groupby('hour')['revenue'].sum().idxmax()
        
        # Pattern logic
        if morning > afternoon and morning > evening:
            pattern = "Morning-driven demand"
        elif evening > morning and evening > afternoon:
            pattern = "Evening-driven demand"
        else:
            pattern = "Balanced demand pattern"
        
        # Store insight
        store_insight.append(
            f"{store}: Peak at {peak_hour} → {pattern}"
        )
    return store_insight

def store_strength(df):
    
    # Total per store
    store_totals = df.groupby('store_location')['revenue'].sum()
    
    avg_total = store_totals.mean()
    
    strength_dict = {}
    
    for store, total in store_totals.items():
        
        if total > avg_total:
            strength_dict[store] = "🔥 High traffic store"
        else:
            strength_dict[store] = "📊 Moderate traffic store"
    
    return strength_dict