import streamlit as st
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from feature_engineer import *
from sales_trends import *
from Day_week_perform import *
from time_demand import *
from cross_location import *


palette =sns.color_palette([
    '#5C4033', #slidebar
    '#FBFBFB', #background/main area
    '#8D6E63', #text
    '#C58E47',#button
    "#8D6E63",  # medium
    "#A1887F"  # soft brown
])
palette_hex = palette.as_hex()

#Title
st.set_page_config(page_title="Afficionado Coffee Dashboard",page_icon=":coffee:",layout='wide')
#-----------Title------------ 
st.title("AFFACIONADO COFFEE ROASTER :coffee:")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>',unsafe_allow_html=True)

#Filter
st.sidebar.header("CHOOSE FILTERS")
location = st.sidebar.multiselect("Store Location",df['store_location'].unique(),default=df['store_location'].unique())
days = st.sidebar.multiselect("Days of week",df['weekday'].unique(), default=df['weekday'].unique())
hours = st.sidebar.slider('Hours Range',0,23,(0,23))
metric = st.sidebar.radio("Metric",['revenue', 'transaction_qty'], format_func=lambda x: x.replace("_", " ").title())

# Apply filters
filtered_df = df[
    (df['store_location'].isin(location)) &
    (df['weekday'].isin(days)) &
    (df['hour'] >= hours[0]) &
    (df['hour'] <= hours[1])
]

#KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"{filtered_df['revenue'].sum():,.2f}")
col2.metric("Total Transaction", f"{filtered_df['transaction_id'].nunique():,}")
col3.metric("Avg Order Value", f"{filtered_df['revenue'].mean():,.3f}")

#tabs
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 200px;  /* Increase space between tabs */
    }
    </style>
""", unsafe_allow_html=True)
tab1, tab2, tab3, tab4 = st.tabs(['Sales Trends', 'Week Performance', 'Hourly Demands', 'Location Analysis'])

with tab1:
    col1 = st.columns(1)
    daily_trends = get_daily_trends(filtered_df)
    st.header(f'Daily {metric.replace('_',' ').title()} Trends')
    fig1= px.line(daily_trends, x='date', y=metric,color_discrete_sequence=px.colors.sequential.Viridis ,labels={'date':'Date', metric: 'Revenue' if metric=='revenue' else 'Transaction'},markers=True)
    st.plotly_chart(fig1,use_container_width=True,key="fig1")

    col1 = st.columns(1)
    with st.expander("Revenue_ViewData"):
        st.write(daily_trends.style.background_gradient(cmap="Blues"))
        csv = daily_trends.to_csv(index=False).encode('utf-8')
        st.download_button("Dowload",data=csv,file_name="Daily Trend.csv",mime="text/csv",help= "Click here to download the CSV file")

    col1,col2 = st.columns(2)
    with col1:
        weekly_Trends = get_weekly_Trend(filtered_df)
        st.header(f"Weekly {metric.replace('_',' ').title()} Trends")
        fig2 = px.bar(weekly_Trends, x='date', y=metric, barmode='group', labels={'date':'Date', metric: 'Revenue' if metric == 'revenue' else 'Transaction'})
        st.plotly_chart(fig2,use_container_width=True,key="fig2")

    with col2:
        monthly_Trends = get_monthly_Trend(filtered_df)
        st.header(f"Monthly {metric.replace('_',' ').title()} Trends")
        fig3 = px.bar(monthly_Trends, x='date', y=metric, barmode='group', labels={'date':'Date', metric: 'Revenue' if metric == 'revenue' else 'Transaction'})
        st.plotly_chart(fig3,use_container_width=True,key="fig3")

    col1 = st.columns(1)
    store_compare = get_store_comparision(filtered_df)
    st.header('Store level daily comparision')
    fig4 = px.line(store_compare, x = 'date', y = metric,color= 'store_location', labels= {'date':'Date',metric: 'Revenue' if metric=='revenue' else 'Transaction'})
    st.plotly_chart(fig4,use_container_width=True,key="fig4")

    col1 = st.columns(1)
    with st.expander("store comparison data"):
        st.write(store_compare.style.background_gradient(cmap="Blues"))
        csv = store_compare.to_csv(index=False).encode('utf-8')
        st.download_button("Dowload",data=csv,file_name="store compare.csv",mime="text/csv",help= "Click here to download the CSV file")


with tab2:
    col1 = st.columns(1)
    weekly_perform = get_weekly_revenue(filtered_df)
    st.header(f"Weekly {metric.replace('_',' ').title()}")
    fig5 = px.bar(weekly_perform, x='weekday', y=metric,category_orders={"weekday" : week_order},labels={'weekday':'Days', metric:'Revenue' if metric=='revenue' else 'Transaction count'})
    st.plotly_chart(fig5,use_container_width=True,key="fig5")

    col1 = st.columns(1)
    with st.expander("Weekly trends data"):
        st.write(weekly_perform.style.background_gradient(cmap="Blues"))
        csv = weekly_perform.to_csv(index=False).encode('utf-8')
        st.download_button("Dowload",data=csv,file_name="weekly revenue.csv",mime="text/csv",help= "Click here to download the CSV file")

    col1 = st.columns(1)
    st.header(f"Week vs Weekend comparison")
    week_weekend = get_week_weekend(filtered_df)
    fig6 = px.bar(week_weekend, x='week', y=metric, labels={'week':'Week vs Weekend', metric: 'Revenue' if metric=='revenue' else 'Transaction'})
    st.plotly_chart(fig6,use_container_width=True,key="fig6")
    
    col1 = st.columns(1)
    with st.expander("Weekly trends data"):
        st.write(week_weekend.style.background_gradient(cmap="Blues"))
        csv = week_weekend.to_csv(index=False).encode('utf-8')
        st.download_button("Dowload",data=csv,file_name="week weekend.csv",mime="text/csv",help= "Click here to download the CSV file")

    col1 = st.columns(1)
    st.header(f"Interpret behaviour of {metric.replace('_',' ').title()} on Workday & Leisure")
    insights = interpret_behaviour(filtered_df)
    for i in insights:
        st.info(i)


with tab3:
    col1 = st.columns(1)
    st.header(f"Hourly {metric.replace('_',' ').title()} analysis")
    hour_analysis = get_hours_analysis(filtered_df)
    fig7 = px.line(hour_analysis, x = 'hour', y = metric, labels={'hour': 'Hours', metric: 'Revenue' if metric=='revenue' else 'Transaction count'})
    st.plotly_chart(fig7,use_container_width=True,key="fig7")

    col1 = st.columns(1)
    with st.expander("Hour analysis data"):
        st.write(hour_analysis.style.background_gradient(cmap="Blues"))
        csv =hour_analysis.to_csv(index=False).encode('utf-8')
        st.download_button("Download",data=csv,file_name="hourly_analysis.csv",mime="text/csv",help="Click here to download the csv file")

    col1 = st.columns(1)
    st.success(f"Morning Rush hour: {insight['morning_revenue_hour']}:00")
    st.info(f"Midday slow period: {insight['midday_revenue_hour']}:00")
    st.success(f"Evening Peak: {insight['evening_revenue_hour']}:00")

with tab4:
    col1 =st.columns(1)
    st.header("Hourly heatmap per store")
    hourly_heatmap = get_hourly_heatmap(filtered_df)
    heatmap_pivot = hourly_heatmap.pivot(index='store_location', columns='hour', values=metric).fillna(0)
    fig8 = px.imshow(heatmap_pivot,aspect='auto',title="Hourly Demand Heatmap",color_continuous_scale='Blues',labels={'store_location': 'Store','hour':'Hour'})
    # fig8 = px.density_heatmap(hourly_heatmap,x='store_location',y=metric,labels={'store_location':'Stores', metric: 'Revenue' if metric=='revenue' else 'Total Transaction'})
    st.plotly_chart(fig8,use_container_width=True,key="fig8")
    col1 = st.columns(1)

    peak_per_store = hourly_heatmap.loc[hourly_heatmap.groupby('store_location')[metric].idxmax()].reset_index()
    st.header("Peak Hour alignment or divergence across locations")
    st.dataframe(peak_per_store[['store_location','hour', metric]])

    unique_peak_hours = peak_per_store['hour'].nunique()

    if unique_peak_hours == 1:
        st.success("✅ All stores have the same peak hour → Aligned Demand Pattern")
    else:
        st.warning("⚠️ Stores have different peak hours → Divergent Demand Pattern")


    # alignment_groups = peak_per_store.groupby('hour')['store_location'].apply(list)
    # aligned = []
    # divergence = []

    # for hour,stores in alignment_groups.items():
    #     if len(stores) > 1:
    #         aligned.append((hour,stores))
    #     else:
    #         divergence.append((hour,stores))
    
    # st.markdown("### Aligned Stores")

    # if aligned:
    #     for hour, stores in aligned:
    #         st.success(f"Hour {hour}: {', '.join(stores)} (Aligned)")
    # else:
    #     st.info("No aligned peak hours found")

    # st.markdown("### Divergent Stores")

    # if divergence:
    #     for hour, stores in divergence:
    #         st.warning(f"Hour {hour}: {', '.join(stores)} (Unique peak)")
    # else:
    #     st.success("All stores are aligned")

    col1 = st.columns(1)
    st.header("Location specificed customers behaviour insight")
    st.subheader("store behaviour on hour")
    customer_behaviour = customer_insight(filtered_df)
    if not customer_behaviour:
        st.warning("No data available for select filter")
    else:
        for customer_insights in customer_behaviour:
            st.info(customer_insights)

    col1 =st.columns(1)
    st.subheader("High traffic store")
    strength_map = store_strength(filtered_df)
    for store, strength in strength_map.items():
        st.info(f"{store}: {strength}")