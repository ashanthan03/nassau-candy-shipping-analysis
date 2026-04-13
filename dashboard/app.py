# ============================================================
# Nassau Candy Distributor — Streamlit Dashboard
# Factory-to-Customer Shipping Route Efficiency Analysis
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Nassau Candy | Shipping Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem; font-weight: 800; color: #1a1a2e;
        text-align: center; padding: 10px 0 5px 0;
    }
    .sub-header {
        font-size: 1rem; color: #555; text-align: center; margin-bottom: 20px;
    }
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px; padding: 20px; color: white; text-align: center;
    }
    .kpi-value { font-size: 2rem; font-weight: 800; }
    .kpi-label { font-size: 0.85rem; opacity: 0.85; }
    .section-title {
        font-size: 1.3rem; font-weight: 700; color: #1a1a2e;
        border-left: 4px solid #667eea; padding-left: 10px; margin: 20px 0 10px 0;
    }
    div[data-testid="metric-container"] {
        background: #f8f9ff; border-radius: 10px; padding: 10px;
        border: 1px solid #e0e4ff;
    }
</style>
""", unsafe_allow_html=True)

# ---- FACTORY MAPPING ----
FACTORY_MAP = {
    'Wonka Bar - Nutty Crunch Surprise'  : "Lot's O' Nuts",
    'Wonka Bar - Fudge Mallows'          : "Lot's O' Nuts",
    'Wonka Bar -Scrumdiddlyumptious'     : "Lot's O' Nuts",
    'Wonka Bar - Milk Chocolate'         : "Wicked Choccy's",
    'Wonka Bar - Triple Dazzle Caramel'  : "Wicked Choccy's",
    'Laffy Taffy'                        : 'Sugar Shack',
    'SweeTARTS'                          : 'Sugar Shack',
    'Nerds'                              : 'Sugar Shack',
    'Fun Dip'                            : 'Sugar Shack',
    'Fizzy Lifting Drinks'               : 'Sugar Shack',
    'Everlasting Gobstopper'             : 'Secret Factory',
    'Hair Toffee'                        : 'The Other Factory',
    'Lickable Wallpaper'                 : 'Secret Factory',
    'Wonka Gum'                          : 'Secret Factory',
    'Kazookles'                          : 'The Other Factory'
}

FACTORY_COLORS = {
    "Lot's O' Nuts"     : '#4C72B0',
    "Wicked Choccy's"   : '#DD8452',
    'Sugar Shack'       : '#55A868',
    'Secret Factory'    : '#C44E52',
    'The Other Factory' : '#8172B2'
}

# ---- DATA LOADING ----
@st.cache_data
def load_data():
    # Try multiple paths (local dev vs deployed)
    import os
    paths = [
        "../data/Nassau_Candy_Distributor.csv",
        "data/Nassau_Candy_Distributor.csv",
        "Nassau_Candy_Distributor.csv"
    ]
    df = None
    for p in paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            break
    if df is None:
        st.error("Dataset not found. Place Nassau_Candy_Distributor.csv in the data/ folder.")
        st.stop()

    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)
    df['Lead Time']  = (df['Ship Date'] - df['Order Date']).dt.days
    df = df[df['Lead Time'] > 0]

    df['Factory']       = df['Product Name'].map(FACTORY_MAP)
    df['Route_State']   = df['Factory'] + ' → ' + df['State/Province']
    df['Route_Region']  = df['Factory'] + ' → ' + df['Region']
    df['Order_Year']    = df['Order Date'].dt.year
    df['Order_Month']   = df['Order Date'].dt.month

    DELAY_THRESHOLD     = df['Lead Time'].median()
    df['Is_Delayed']    = df['Lead Time'] > DELAY_THRESHOLD

    return df, DELAY_THRESHOLD

df, DELAY_THRESHOLD = load_data()

# ============================================================
# SIDEBAR — FILTERS
# ============================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Candy_in_Damascus.jpg/320px-Candy_in_Damascus.jpg",
                 use_column_width=True)
st.sidebar.markdown("## 🍬 Nassau Candy")
st.sidebar.markdown("### Filters")

# Date filter
min_date = df['Order Date'].min().date()
max_date = df['Order Date'].max().date()
date_range = st.sidebar.date_input("📅 Order Date Range",
    value=[min_date, max_date], min_value=min_date, max_value=max_date)

# Region filter
all_regions = sorted(df['Region'].unique())
sel_regions = st.sidebar.multiselect("🌍 Region", all_regions, default=all_regions)

# Ship Mode filter
all_modes = sorted(df['Ship Mode'].unique())
sel_modes = st.sidebar.multiselect("🚚 Ship Mode", all_modes, default=all_modes)

# Factory filter
all_factories = sorted(df['Factory'].unique())
sel_factories = st.sidebar.multiselect("🏭 Factory", all_factories, default=all_factories)

# Delay threshold slider
custom_delay = st.sidebar.slider(
    "⚠️ Delay Threshold (days)",
    min_value=int(df['Lead Time'].min()),
    max_value=int(df['Lead Time'].max()),
    value=int(DELAY_THRESHOLD),
    step=10
)

st.sidebar.markdown("---")
st.sidebar.caption(f"📊 Dataset: 10,194 orders | 196 routes")
st.sidebar.caption(f"📅 Period: Jan 2024 – Dec 2025")

# ---- APPLY FILTERS ----
if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date = pd.Timestamp(min_date)
    end_date   = pd.Timestamp(max_date)

mask = (
    (df['Order Date'] >= start_date) &
    (df['Order Date'] <= end_date) &
    (df['Region'].isin(sel_regions)) &
    (df['Ship Mode'].isin(sel_modes)) &
    (df['Factory'].isin(sel_factories))
)
fdf = df[mask].copy()
fdf['Is_Delayed'] = fdf['Lead Time'] > custom_delay

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="main-header">🍬 Nassau Candy Distributor</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Factory-to-Customer Shipping Route Efficiency Dashboard</div>', unsafe_allow_html=True)
st.markdown("---")

if len(fdf) == 0:
    st.warning("No data matches your filters. Please adjust the sidebar filters.")
    st.stop()

# ============================================================
# TOP KPI CARDS
# ============================================================
k1, k2, k3, k4, k5 = st.columns(5)

avg_lt      = fdf['Lead Time'].mean()
delay_rate  = fdf['Is_Delayed'].mean() * 100
total_sales = fdf['Sales'].sum()
total_ord   = len(fdf)
unique_rt   = fdf['Route_State'].nunique()

k1.metric("📦 Total Orders",      f"{total_ord:,}")
k2.metric("⏱ Avg Lead Time",      f"{avg_lt:.0f} days")
k3.metric("⚠️ Delay Rate",         f"{delay_rate:.1f}%")
k4.metric("💰 Total Sales",        f"${total_sales:,.0f}")
k5.metric("🗺 Active Routes",      f"{unique_rt}")

st.markdown("---")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Route Efficiency",
    "🗺 Geographic Map",
    "🚚 Ship Mode Analysis",
    "🔍 Route Drill-Down",
    "📈 Trends & Insights"
])

# ============================================================
# TAB 1 — ROUTE EFFICIENCY OVERVIEW
# ============================================================
with tab1:
    st.markdown('<div class="section-title">Route Efficiency Leaderboard</div>', unsafe_allow_html=True)

    route_agg = fdf.groupby('Route_State').agg(
        Factory          = ('Factory', 'first'),
        State            = ('State/Province', 'first'),
        Region           = ('Region', 'first'),
        Total_Shipments  = ('Order ID', 'count'),
        Avg_Lead_Time    = ('Lead Time', 'mean'),
        Std_Lead_Time    = ('Lead Time', 'std'),
        Delay_Rate       = ('Is_Delayed', 'mean'),
        Total_Sales      = ('Sales', 'sum'),
        Avg_Profit       = ('Gross Profit', 'mean')
    ).reset_index()

    scaler = MinMaxScaler()
    route_agg['Efficiency_Score'] = (
        1 - scaler.fit_transform(route_agg[['Avg_Lead_Time']])
    ).round(4)
    route_agg = route_agg.sort_values('Avg_Lead_Time')

    top10    = route_agg.head(10)
    bottom10 = route_agg.tail(10)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ✅ Top 10 Most Efficient Routes")
        fig = px.bar(
            top10, x='Avg_Lead_Time', y='Route_State',
            orientation='h', color='Factory',
            color_discrete_map=FACTORY_COLORS,
            text=top10['Avg_Lead_Time'].round(0).astype(int).astype(str) + "d",
            title="Lowest Average Lead Time"
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'},
                          showlegend=False, height=380,
                          margin=dict(l=10, r=10, t=40, b=10))
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### ❌ Bottom 10 Least Efficient Routes")
        fig2 = px.bar(
            bottom10, x='Avg_Lead_Time', y='Route_State',
            orientation='h', color='Factory',
            color_discrete_map=FACTORY_COLORS,
            text=bottom10['Avg_Lead_Time'].round(0).astype(int).astype(str) + "d",
            title="Highest Average Lead Time"
        )
        fig2.update_layout(yaxis={'categoryorder': 'total descending'},
                           showlegend=False, height=380,
                           margin=dict(l=10, r=10, t=40, b=10))
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Full Route Performance Table")

    display_cols = ['Route_State','Factory','Region','Total_Shipments',
                    'Avg_Lead_Time','Delay_Rate','Efficiency_Score','Avg_Profit']
    display_df = route_agg[display_cols].copy()
    display_df['Avg_Lead_Time'] = display_df['Avg_Lead_Time'].round(1)
    display_df['Delay_Rate']    = (display_df['Delay_Rate'] * 100).round(1).astype(str) + '%'
    display_df['Efficiency_Score'] = display_df['Efficiency_Score'].round(4)
    display_df['Avg_Profit']    = '$' + display_df['Avg_Profit'].round(2).astype(str)
    display_df.columns = ['Route','Factory','Region','Shipments',
                          'Avg Lead (days)','Delay Rate','Efficiency Score','Avg Profit']

    st.dataframe(display_df, use_container_width=True, height=400)

    # Factory comparison
    st.markdown("---")
    st.markdown("#### 🏭 Factory Performance Summary")
    fac_col1, fac_col2 = st.columns(2)

    factory_stats = fdf.groupby('Factory').agg(
        Avg_Lead_Time   = ('Lead Time', 'mean'),
        Total_Shipments = ('Order ID', 'count'),
        Delay_Rate      = ('Is_Delayed', 'mean'),
        Total_Sales     = ('Sales', 'sum')
    ).reset_index().sort_values('Avg_Lead_Time')

    with fac_col1:
        fig3 = px.bar(factory_stats, x='Factory', y='Avg_Lead_Time',
                      color='Factory', color_discrete_map=FACTORY_COLORS,
                      title='Avg Lead Time by Factory',
                      text=factory_stats['Avg_Lead_Time'].round(0).astype(int))
        fig3.update_layout(showlegend=False, height=350)
        fig3.update_traces(textposition='outside')
        st.plotly_chart(fig3, use_container_width=True)

    with fac_col2:
        fig4 = px.pie(factory_stats, names='Factory', values='Total_Shipments',
                      color='Factory', color_discrete_map=FACTORY_COLORS,
                      title='Shipment Volume Share by Factory')
        fig4.update_layout(height=350)
        st.plotly_chart(fig4, use_container_width=True)

# ============================================================
# TAB 2 — GEOGRAPHIC MAP
# ============================================================
with tab2:
    st.markdown('<div class="section-title">Geographic Shipping Efficiency Map</div>', unsafe_allow_html=True)

    # State abbreviation mapping
    state_abbr = {
        'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
        'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
        'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
        'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
        'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
        'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
        'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
        'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
        'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
        'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
        'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
        'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
        'Wisconsin': 'WI', 'Wyoming': 'WY', 'District of Columbia': 'DC'
    }

    state_data = fdf.groupby('State/Province').agg(
        Avg_Lead_Time   = ('Lead Time', 'mean'),
        Total_Shipments = ('Order ID', 'count'),
        Delay_Rate      = ('Is_Delayed', 'mean'),
        Total_Sales     = ('Sales', 'sum')
    ).reset_index()
    state_data['Abbr']       = state_data['State/Province'].map(state_abbr)
    state_data['Delay_Pct']  = (state_data['Delay_Rate'] * 100).round(1)
    state_data = state_data.dropna(subset=['Abbr'])

    map_metric = st.radio("Color map by:", 
        ["Avg Lead Time", "Shipment Volume", "Delay Rate (%)"],
        horizontal=True)

    metric_col_map = {
        "Avg Lead Time"      : ('Avg_Lead_Time', 'RdYlGn_r', 'Avg Lead Time (days)'),
        "Shipment Volume"    : ('Total_Shipments', 'Blues',   'Total Shipments'),
        "Delay Rate (%)"     : ('Delay_Pct',       'Reds',    'Delay Rate (%)')
    }
    col, cscale, label = metric_col_map[map_metric]

    fig_map = px.choropleth(
        state_data,
        locations='Abbr',
        locationmode='USA-states',
        color=col,
        scope='usa',
        color_continuous_scale=cscale,
        hover_name='State/Province',
        hover_data={
            'Abbr': False,
            'Avg_Lead_Time': ':.0f',
            'Total_Shipments': True,
            'Delay_Pct': True
        },
        title=f'US Heatmap — {label}'
    )
    fig_map.update_layout(height=500, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

    # Factory locations scatter
    st.markdown("---")
    st.markdown("#### 🏭 Factory Locations")
    factory_df = pd.DataFrame([
        {"Factory": "Lot's O' Nuts",    "Lat": 32.881893, "Lon": -111.768036, "State": "Arizona"},
        {"Factory": "Wicked Choccy's",  "Lat": 32.076176, "Lon": -81.088371,  "State": "Georgia"},
        {"Factory": "Sugar Shack",      "Lat": 48.11914,  "Lon": -96.18115,   "State": "Minnesota/ND"},
        {"Factory": "Secret Factory",   "Lat": 41.446333, "Lon": -90.565487,  "State": "Illinois"},
        {"Factory": "The Other Factory","Lat": 35.1175,   "Lon": -89.971107,  "State": "Tennessee"}
    ])
    factory_df['Color'] = factory_df['Factory'].map(FACTORY_COLORS)
    factory_df['Shipments'] = factory_df['Factory'].map(
        fdf['Factory'].value_counts().to_dict()
    ).fillna(0).astype(int)

    fig_fac = px.scatter_geo(
        factory_df, lat='Lat', lon='Lon',
        scope='usa', size='Shipments',
        color='Factory', color_discrete_map=FACTORY_COLORS,
        hover_name='Factory',
        hover_data={'Lat': False, 'Lon': False, 'State': True, 'Shipments': True},
        size_max=50,
        title='Factory Locations & Shipment Volume'
    )
    fig_fac.update_layout(height=450)
    st.plotly_chart(fig_fac, use_container_width=True)

    # Top/Bottom states table
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### ✅ Top 10 Fastest Delivery States")
        top_states = state_data.nsmallest(10, 'Avg_Lead_Time')[
            ['State/Province','Avg_Lead_Time','Total_Shipments','Delay_Pct']
        ].rename(columns={'State/Province':'State','Avg_Lead_Time':'Avg Lead (days)',
                          'Total_Shipments':'Shipments','Delay_Pct':'Delay %'})
        st.dataframe(top_states.reset_index(drop=True), use_container_width=True)

    with col_b:
        st.markdown("#### ❌ Top 10 Slowest Delivery States")
        bot_states = state_data.nlargest(10, 'Avg_Lead_Time')[
            ['State/Province','Avg_Lead_Time','Total_Shipments','Delay_Pct']
        ].rename(columns={'State/Province':'State','Avg_Lead_Time':'Avg Lead (days)',
                          'Total_Shipments':'Shipments','Delay_Pct':'Delay %'})
        st.dataframe(bot_states.reset_index(drop=True), use_container_width=True)

# ============================================================
# TAB 3 — SHIP MODE ANALYSIS
# ============================================================
with tab3:
    st.markdown('<div class="section-title">Ship Mode Performance Comparison</div>', unsafe_allow_html=True)

    mode_stats = fdf.groupby('Ship Mode').agg(
        Avg_Lead_Time   = ('Lead Time', 'mean'),
        Median_Lead     = ('Lead Time', 'median'),
        Std_Lead        = ('Lead Time', 'std'),
        Total_Shipments = ('Order ID', 'count'),
        Delay_Rate      = ('Is_Delayed', 'mean'),
        Avg_Sales       = ('Sales', 'mean'),
        Total_Sales     = ('Sales', 'sum')
    ).reset_index().sort_values('Avg_Lead_Time')

    c1, c2, c3 = st.columns(3)
    best_mode  = mode_stats.iloc[0]['Ship Mode']
    worst_mode = mode_stats.iloc[-1]['Ship Mode']
    c1.metric("🏆 Fastest Ship Mode",  best_mode,  f"{mode_stats.iloc[0]['Avg_Lead_Time']:.0f} days avg")
    c2.metric("🐢 Slowest Ship Mode", worst_mode,  f"{mode_stats.iloc[-1]['Avg_Lead_Time']:.0f} days avg")
    c3.metric("📦 Most Used Mode",
              mode_stats.loc[mode_stats['Total_Shipments'].idxmax(), 'Ship Mode'],
              f"{mode_stats['Total_Shipments'].max():,} shipments")

    st.markdown("---")
    r1c1, r1c2 = st.columns(2)

    with r1c1:
        # Box plot via plotly
        box_data = []
        for mode in fdf['Ship Mode'].unique():
            box_data.append(go.Box(
                y=fdf[fdf['Ship Mode']==mode]['Lead Time'],
                name=mode, boxmean=True
            ))
        fig_box = go.Figure(data=box_data)
        fig_box.update_layout(title='Lead Time Distribution by Ship Mode',
                              yaxis_title='Lead Time (Days)', height=380)
        st.plotly_chart(fig_box, use_container_width=True)

    with r1c2:
        fig_bar = px.bar(mode_stats, x='Ship Mode', y='Avg_Lead_Time',
                         color='Ship Mode', text=mode_stats['Avg_Lead_Time'].round(0).astype(int),
                         title='Avg Lead Time by Ship Mode')
        fig_bar.update_layout(showlegend=False, height=380, yaxis_title='Avg Lead Time (Days)')
        fig_bar.update_traces(textposition='outside')
        st.plotly_chart(fig_bar, use_container_width=True)

    r2c1, r2c2 = st.columns(2)
    with r2c1:
        fig_delay = px.bar(mode_stats, x='Ship Mode',
                           y=(mode_stats['Delay_Rate']*100).round(1),
                           color='Ship Mode', title='Delay Rate by Ship Mode (%)',
                           text=(mode_stats['Delay_Rate']*100).round(1).astype(str)+'%')
        fig_delay.update_layout(showlegend=False, height=350, yaxis_title='Delay Rate (%)')
        fig_delay.update_traces(textposition='outside')
        st.plotly_chart(fig_delay, use_container_width=True)

    with r2c2:
        fig_vol = px.pie(mode_stats, names='Ship Mode', values='Total_Shipments',
                         title='Shipment Volume Share by Ship Mode')
        fig_vol.update_layout(height=350)
        st.plotly_chart(fig_vol, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Ship Mode × Region Cross Analysis")
    pivot = fdf.groupby(['Ship Mode', 'Region'])['Lead Time'].mean().round(1).unstack()
    st.dataframe(pivot.style.background_gradient(cmap='RdYlGn_r', axis=None), 
                 use_container_width=True)

# ============================================================
# TAB 4 — ROUTE DRILL-DOWN
# ============================================================
with tab4:
    st.markdown('<div class="section-title">Route Drill-Down — State & Order Level</div>', unsafe_allow_html=True)

    drill_col1, drill_col2 = st.columns([1, 2])

    with drill_col1:
        selected_factory = st.selectbox("🏭 Select Factory", sorted(fdf['Factory'].unique()))
        factory_states   = sorted(fdf[fdf['Factory']==selected_factory]['State/Province'].unique())
        selected_state   = st.selectbox("📍 Select State", factory_states)

    route_df = fdf[
        (fdf['Factory'] == selected_factory) &
        (fdf['State/Province'] == selected_state)
    ].copy()

    with drill_col2:
        if len(route_df) > 0:
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Total Orders",  f"{len(route_df):,}")
            r2.metric("Avg Lead Time", f"{route_df['Lead Time'].mean():.0f} days")
            r3.metric("Delay Rate",    f"{route_df['Is_Delayed'].mean()*100:.1f}%")
            r4.metric("Total Sales",   f"${route_df['Sales'].sum():,.0f}")

    if len(route_df) > 0:
        st.markdown(f"#### Route: **{selected_factory} → {selected_state}**")

        t1, t2 = st.columns(2)
        with t1:
            fig_hist = px.histogram(route_df, x='Lead Time', nbins=20,
                                    color_discrete_sequence=['steelblue'],
                                    title='Lead Time Distribution for this Route')
            fig_hist.add_vline(x=route_df['Lead Time'].mean(), line_dash='dash',
                               line_color='red', annotation_text='Mean')
            fig_hist.update_layout(height=300)
            st.plotly_chart(fig_hist, use_container_width=True)

        with t2:
            mode_rt = route_df.groupby('Ship Mode')['Lead Time'].mean().reset_index()
            fig_rt_mode = px.bar(mode_rt, x='Ship Mode', y='Lead Time',
                                 color='Ship Mode', title='Lead Time by Ship Mode (this route)',
                                 text=mode_rt['Lead Time'].round(0).astype(int))
            fig_rt_mode.update_layout(showlegend=False, height=300)
            fig_rt_mode.update_traces(textposition='outside')
            st.plotly_chart(fig_rt_mode, use_container_width=True)

        st.markdown("#### 📦 Order-Level Shipment Timeline")
        timeline_df = route_df[[
            'Order ID', 'Order Date', 'Ship Date', 'Lead Time',
            'Product Name', 'Ship Mode', 'Sales', 'Gross Profit', 'Is_Delayed'
        ]].sort_values('Order Date').copy()
        timeline_df['Is_Delayed'] = timeline_df['Is_Delayed'].map({True:'⚠️ Delayed', False:'✅ On Time'})
        timeline_df['Order Date'] = timeline_df['Order Date'].dt.strftime('%Y-%m-%d')
        timeline_df['Ship Date']  = timeline_df['Ship Date'].dt.strftime('%Y-%m-%d')
        timeline_df['Sales']      = '$' + timeline_df['Sales'].round(2).astype(str)
        timeline_df['Gross Profit'] = '$' + timeline_df['Gross Profit'].round(2).astype(str)
        st.dataframe(timeline_df.rename(columns={'Is_Delayed':'Status'}),
                     use_container_width=True, height=350)
    else:
        st.info("No orders found for this factory-state combination with current filters.")

# ============================================================
# TAB 5 — TRENDS & INSIGHTS
# ============================================================
with tab5:
    st.markdown('<div class="section-title">Temporal Trends & Business Insights</div>', unsafe_allow_html=True)

    # Monthly trends
    monthly = fdf.groupby(['Order_Year','Order_Month']).agg(
        Avg_Lead_Time = ('Lead Time','mean'),
        Order_Count   = ('Order ID','count'),
        Total_Sales   = ('Sales','sum')
    ).reset_index()
    monthly['Period'] = (monthly['Order_Year'].astype(str) + '-' +
                         monthly['Order_Month'].astype(str).str.zfill(2))
    monthly = monthly.sort_values(['Order_Year','Order_Month'])

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(go.Scatter(x=monthly['Period'], y=monthly['Avg_Lead_Time'],
                                   name='Avg Lead Time', line=dict(color='steelblue', width=2.5),
                                   mode='lines+markers'), secondary_y=False)
    fig_trend.add_trace(go.Bar(x=monthly['Period'], y=monthly['Order_Count'],
                               name='Order Volume', marker_color='rgba(255,165,0,0.4)',
                               opacity=0.6), secondary_y=True)
    fig_trend.update_layout(title='Monthly Avg Lead Time vs Order Volume',
                            height=380, xaxis_tickangle=45)
    fig_trend.update_yaxes(title_text='Avg Lead Time (Days)', secondary_y=False)
    fig_trend.update_yaxes(title_text='Order Volume',          secondary_y=True)
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("---")
    ins_c1, ins_c2 = st.columns(2)

    with ins_c1:
        # Division performance
        div_data = fdf.groupby('Division').agg(
            Avg_Lead_Time = ('Lead Time','mean'),
            Total_Orders  = ('Order ID','count'),
            Avg_Profit    = ('Gross Profit','mean')
        ).reset_index()
        fig_div = px.scatter(div_data, x='Avg_Lead_Time', y='Avg_Profit',
                             size='Total_Orders', color='Division',
                             text='Division', title='Division: Lead Time vs Profitability',
                             size_max=60)
        fig_div.update_traces(textposition='top center')
        fig_div.update_layout(height=380)
        st.plotly_chart(fig_div, use_container_width=True)

    with ins_c2:
        # Correlation
        corr_df = fdf[['Lead Time','Sales','Units','Gross Profit','Cost']].corr()
        fig_corr = px.imshow(corr_df, text_auto='.2f', color_continuous_scale='RdBu_r',
                             title='Correlation Heatmap', zmin=-1, zmax=1)
        fig_corr.update_layout(height=380)
        st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("---")
    st.markdown("### 💡 Key Business Insights")

    insight_c1, insight_c2, insight_c3 = st.columns(3)

    with insight_c1:
        st.info("""
**🏆 Best Performing Factory**

**The Other Factory** (Tennessee) achieves the 
lowest average lead time of **1,280 days**, 
outperforming all other factories despite 
handling only 100 shipments.
        """)

    with insight_c2:
        st.warning("""
**⚠️ Geographic Bottleneck**

**Sugar Shack** (Minnesota) routes to 
Northeast states (CT, NJ, NH) show the 
worst lead times at **1,641–1,642 days**, 
possibly due to extreme geographic distance.
        """)

    with insight_c3:
        st.success("""
**📦 Ship Mode Paradox**

**Standard Class** is counterintuitively the 
fastest ship mode (avg 1,314 days) vs 
**First Class** at 1,338 days. This suggests 
scheduling or routing differences rather 
than actual transit speed.
        """)

    st.markdown("---")
    st.markdown("### 📋 Executive Summary Statistics")
    summary = {
        'Metric': ['Total Orders', 'Unique Routes', 'Avg Lead Time', 'Fastest Factory',
                   'Slowest Factory', 'Best Region', 'Worst Ship Mode', 'Top State by Volume'],
        'Value':  [f"{len(fdf):,}", f"{fdf['Route_State'].nunique()}",
                   f"{fdf['Lead Time'].mean():.0f} days",
                   fdf.groupby('Factory')['Lead Time'].mean().idxmin(),
                   fdf.groupby('Factory')['Lead Time'].mean().idxmax(),
                   fdf.groupby('Region')['Lead Time'].mean().idxmin(),
                   fdf.groupby('Ship Mode')['Lead Time'].mean().idxmax(),
                   fdf['State/Province'].value_counts().idxmax()]
    }
    st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

# ---- FOOTER ----
st.markdown("---")
st.markdown(
    "<center><small>Nassau Candy Distributor | Shipping Route Efficiency Dashboard | "
    "Built with Streamlit & Plotly</small></center>",
    unsafe_allow_html=True
)
