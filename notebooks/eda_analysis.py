# ============================================================
# Nassau Candy Distributor — Full EDA Analysis
# Factory-to-Customer Shipping Route Efficiency
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Plot styling
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
sns.set_palette("Set2")

# ============================================================
# STEP 1 — LOAD & CLEAN DATA
# ============================================================
print("=" * 60)
print("STEP 1: LOADING AND CLEANING DATA")
print("=" * 60)

df = pd.read_csv("../data/Nassau_Candy_Distributor.csv")

print(f"Raw dataset shape: {df.shape}")
print(f"\nColumn names:\n{list(df.columns)}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nData types:\n{df.dtypes}")

# Date parsing — DD-MM-YYYY format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date']  = pd.to_datetime(df['Ship Date'],  dayfirst=True)

# Lead time
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

# Remove invalid lead times
before = len(df)
df = df[df['Lead Time'] > 0]
print(f"\nRows removed (invalid lead time): {before - len(df)}")
print(f"Clean dataset shape: {df.shape}")
print(f"\nLead Time stats:\n{df['Lead Time'].describe().round(2)}")

# ============================================================
# STEP 2 — FEATURE ENGINEERING
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: FEATURE ENGINEERING")
print("=" * 60)

factory_map = {
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

factory_coords = {
    "Lot's O' Nuts"     : (32.881893, -111.768036),
    "Wicked Choccy's"   : (32.076176, -81.088371),
    'Sugar Shack'        : (48.11914,  -96.18115),
    'Secret Factory'     : (41.446333, -90.565487),
    'The Other Factory'  : (35.1175,   -89.971107)
}

df['Factory']        = df['Product Name'].map(factory_map)
df['Route_State']    = df['Factory'] + ' -> ' + df['State/Province']
df['Route_Region']   = df['Factory'] + ' -> ' + df['Region']
df['Order_Year']     = df['Order Date'].dt.year
df['Order_Month']    = df['Order Date'].dt.month
df['Order_Quarter']  = df['Order Date'].dt.to_period('Q').astype(str)

DELAY_THRESHOLD      = df['Lead Time'].median()   # 1274 days
df['Is_Delayed']     = df['Lead Time'] > DELAY_THRESHOLD

print(f"Delay threshold (median): {DELAY_THRESHOLD} days")
print(f"Delayed shipments: {df['Is_Delayed'].sum()} ({df['Is_Delayed'].mean()*100:.1f}%)")
print(f"\nFactory distribution:\n{df['Factory'].value_counts()}")
print(f"\nUnique routes: {df['Route_State'].nunique()}")

# ============================================================
# STEP 3 — ROUTE AGGREGATION & KPIs
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: ROUTE AGGREGATION & KPIs")
print("=" * 60)

from sklearn.preprocessing import MinMaxScaler

route_agg = df.groupby('Route_State').agg(
    Factory            = ('Factory', 'first'),
    State              = ('State/Province', 'first'),
    Region             = ('Region', 'first'),
    Total_Shipments    = ('Order ID', 'count'),
    Avg_Lead_Time      = ('Lead Time', 'mean'),
    Std_Lead_Time      = ('Lead Time', 'std'),
    Min_Lead_Time      = ('Lead Time', 'min'),
    Max_Lead_Time      = ('Lead Time', 'max'),
    Delay_Rate         = ('Is_Delayed', 'mean'),
    Total_Sales        = ('Sales', 'sum'),
    Avg_Gross_Profit   = ('Gross Profit', 'mean'),
    Total_Units        = ('Units', 'sum')
).reset_index()

scaler = MinMaxScaler()
route_agg['Efficiency_Score'] = 1 - scaler.fit_transform(route_agg[['Avg_Lead_Time']])
route_agg = route_agg.sort_values('Avg_Lead_Time')

top10    = route_agg.head(10).copy()
bottom10 = route_agg.tail(10).copy()

print("\nTOP 10 MOST EFFICIENT ROUTES:")
print(top10[['Route_State','Avg_Lead_Time','Total_Shipments','Efficiency_Score']].to_string(index=False))
print("\nBOTTOM 10 LEAST EFFICIENT ROUTES:")
print(bottom10[['Route_State','Avg_Lead_Time','Total_Shipments','Efficiency_Score']].to_string(index=False))

# Save to CSV
route_agg.to_csv('../outputs/reports/route_kpis.csv', index=False)
print("\nRoute KPIs saved to outputs/reports/route_kpis.csv")

# ============================================================
# STEP 4 — VISUALIZATIONS
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: GENERATING VISUALIZATIONS")
print("=" * 60)

colors = {
    "Lot's O' Nuts"     : '#4C72B0',
    "Wicked Choccy's"   : '#DD8452',
    'Sugar Shack'        : '#55A868',
    'Secret Factory'     : '#C44E52',
    'The Other Factory'  : '#8172B2'
}

# ---- Chart 1: Lead Time Distribution ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['Lead Time'], bins=40, color='steelblue', edgecolor='white', alpha=0.85)
axes[0].axvline(df['Lead Time'].mean(),   color='red',    linestyle='--', linewidth=1.5, label=f"Mean: {df['Lead Time'].mean():.0f}")
axes[0].axvline(df['Lead Time'].median(), color='orange', linestyle='--', linewidth=1.5, label=f"Median: {df['Lead Time'].median():.0f}")
axes[0].set_title('Distribution of Shipping Lead Times', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Lead Time (Days)')
axes[0].set_ylabel('Number of Shipments')
axes[0].legend()

axes[1].boxplot(df['Lead Time'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='lightblue'),
                medianprops=dict(color='red', linewidth=2))
axes[1].set_title('Lead Time Box Plot', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Lead Time (Days)')
axes[1].set_xticks([1]); axes[1].set_xticklabels(['All Shipments'])

plt.tight_layout()
plt.savefig('../outputs/charts/01_lead_time_distribution.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 1: Lead time distribution saved")

# ---- Chart 2: Ship Mode Comparison ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

mode_avg = df.groupby('Ship Mode')['Lead Time'].mean().sort_values()
bars = axes[0].barh(mode_avg.index, mode_avg.values, color=sns.color_palette("Set2", 4))
axes[0].set_title('Average Lead Time by Ship Mode', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Avg Lead Time (Days)')
for bar, val in zip(bars, mode_avg.values):
    axes[0].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}', va='center', fontsize=10)

ship_mode_data = [df[df['Ship Mode'] == m]['Lead Time'].values for m in df['Ship Mode'].unique()]
bp = axes[1].boxplot(ship_mode_data, labels=df['Ship Mode'].unique(), patch_artist=True,
                     medianprops=dict(color='red', linewidth=2))
for patch, color in zip(bp['boxes'], sns.color_palette("Set2", 4)):
    patch.set_facecolor(color)
axes[1].set_title('Lead Time Spread by Ship Mode', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Lead Time (Days)')
axes[1].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig('../outputs/charts/02_ship_mode_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 2: Ship mode comparison saved")

# ---- Chart 3: Factory Performance ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

factory_avg = df.groupby('Factory')['Lead Time'].mean().sort_values()
bar_colors  = [colors[f] for f in factory_avg.index]
bars = axes[0].barh(factory_avg.index, factory_avg.values, color=bar_colors)
axes[0].set_title('Average Lead Time by Factory', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Avg Lead Time (Days)')
for bar, val in zip(bars, factory_avg.values):
    axes[0].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}', va='center', fontsize=10)

factory_vol = df['Factory'].value_counts()
wedge_colors = [colors[f] for f in factory_vol.index]
axes[1].pie(factory_vol.values, labels=factory_vol.index, colors=wedge_colors,
            autopct='%1.1f%%', startangle=140,
            wedgeprops=dict(edgecolor='white', linewidth=1.5))
axes[1].set_title('Shipment Volume by Factory', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/charts/03_factory_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 3: Factory performance saved")

# ---- Chart 4: Regional Performance ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

region_avg = df.groupby('Region')['Lead Time'].mean().sort_values()
bars = axes[0].bar(region_avg.index, region_avg.values, color=sns.color_palette("husl", 4), edgecolor='white')
axes[0].set_title('Average Lead Time by Region', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Avg Lead Time (Days)')
axes[0].set_ylim([region_avg.min() * 0.98, region_avg.max() * 1.02])
for bar, val in zip(bars, region_avg.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, val + 1, f'{val:.0f}', ha='center', fontsize=11, fontweight='bold')

pivot = df.groupby(['Region', 'Ship Mode'])['Lead Time'].mean().unstack()
pivot.plot(kind='bar', ax=axes[1], colormap='Set2', edgecolor='white')
axes[1].set_title('Lead Time: Region × Ship Mode', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Avg Lead Time (Days)')
axes[1].tick_params(axis='x', rotation=15)
axes[1].legend(title='Ship Mode', fontsize=9)

plt.tight_layout()
plt.savefig('../outputs/charts/04_regional_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 4: Regional performance saved")

# ---- Chart 5: Top 10 / Bottom 10 Routes ----
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

top10_sorted = top10.sort_values('Avg_Lead_Time', ascending=True)
bar_colors_top = [colors[f] for f in top10_sorted['Factory']]
bars = axes[0].barh(top10_sorted['Route_State'], top10_sorted['Avg_Lead_Time'], color=bar_colors_top)
axes[0].set_title('Top 10 Most Efficient Routes', fontsize=13, fontweight='bold', color='green')
axes[0].set_xlabel('Avg Lead Time (Days)')
for bar, val in zip(bars, top10_sorted['Avg_Lead_Time']):
    axes[0].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}d', va='center', fontsize=9)

bottom10_sorted = bottom10.sort_values('Avg_Lead_Time', ascending=False)
bar_colors_bot  = [colors[f] for f in bottom10_sorted['Factory']]
bars = axes[1].barh(bottom10_sorted['Route_State'], bottom10_sorted['Avg_Lead_Time'], color=bar_colors_bot)
axes[1].set_title('Bottom 10 Least Efficient Routes', fontsize=13, fontweight='bold', color='red')
axes[1].set_xlabel('Avg Lead Time (Days)')
for bar, val in zip(bars, bottom10_sorted['Avg_Lead_Time']):
    axes[1].text(val + 1, bar.get_y() + bar.get_height()/2, f'{val:.0f}d', va='center', fontsize=9)

# Legend for factories
handles = [mpatches.Patch(color=v, label=k) for k, v in colors.items()]
fig.legend(handles=handles, loc='lower center', ncol=5, fontsize=9, title='Factory',
           bbox_to_anchor=(0.5, -0.02))

plt.tight_layout()
plt.savefig('../outputs/charts/05_top_bottom_routes.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 5: Top/Bottom routes saved")

# ---- Chart 6: Delay Analysis ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

delay_factory = df.groupby('Factory')['Is_Delayed'].mean().sort_values() * 100
bar_colors_d  = [colors[f] for f in delay_factory.index]
bars = axes[0].barh(delay_factory.index, delay_factory.values, color=bar_colors_d)
axes[0].set_title('Delay Rate by Factory (%)', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Delay Rate (%)')
for bar, val in zip(bars, delay_factory.values):
    axes[0].text(val + 0.2, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10)

delay_mode = df.groupby('Ship Mode')['Is_Delayed'].mean().sort_values() * 100
bars = axes[1].bar(delay_mode.index, delay_mode.values, color=sns.color_palette("Set2", 4), edgecolor='white')
axes[1].set_title('Delay Rate by Ship Mode (%)', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Delay Rate (%)')
axes[1].tick_params(axis='x', rotation=15)
for bar, val in zip(bars, delay_mode.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.2, f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/charts/06_delay_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 6: Delay analysis saved")

# ---- Chart 7: Monthly Trend ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

monthly = df.groupby(['Order_Year', 'Order_Month'])['Lead Time'].mean().reset_index()
monthly['Period'] = monthly['Order_Year'].astype(str) + '-' + monthly['Order_Month'].astype(str).str.zfill(2)
monthly = monthly.sort_values(['Order_Year','Order_Month'])
axes[0].plot(monthly['Period'], monthly['Lead Time'], marker='o', linewidth=2, color='steelblue', markersize=5)
axes[0].set_title('Average Lead Time Over Time', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Avg Lead Time (Days)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].set_xticks(axes[0].get_xticks()[::3])

vol_monthly = df.groupby(['Order_Year','Order_Month'])['Order ID'].count().reset_index()
vol_monthly['Period'] = vol_monthly['Order_Year'].astype(str) + '-' + vol_monthly['Order_Month'].astype(str).str.zfill(2)
vol_monthly = vol_monthly.sort_values(['Order_Year','Order_Month'])
axes[1].bar(vol_monthly['Period'], vol_monthly['Order ID'], color='coral', edgecolor='white', alpha=0.8)
axes[1].set_title('Monthly Shipment Volume', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Number of Orders')
axes[1].tick_params(axis='x', rotation=45)
axes[1].set_xticks(axes[1].get_xticks()[::3])

plt.tight_layout()
plt.savefig('../outputs/charts/07_time_trends.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 7: Time trends saved")

# ---- Chart 8: Top 15 States by Volume + Avg Lead Time ----
fig, ax1 = plt.subplots(figsize=(14, 6))
top_states = df['State/Province'].value_counts().head(15).index
state_data  = df[df['State/Province'].isin(top_states)].groupby('State/Province').agg(
    Volume=('Order ID','count'), Avg_LT=('Lead Time','mean')).sort_values('Volume', ascending=False)

ax2 = ax1.twinx()
bars = ax1.bar(state_data.index, state_data['Volume'], color='steelblue', alpha=0.7, label='Shipment Volume')
line = ax2.plot(state_data.index, state_data['Avg_LT'], color='red', marker='o',
                linewidth=2, markersize=7, label='Avg Lead Time')
ax1.set_title('Top 15 States: Volume vs Avg Lead Time', fontsize=13, fontweight='bold')
ax1.set_ylabel('Shipment Volume', color='steelblue')
ax2.set_ylabel('Avg Lead Time (Days)', color='red')
ax1.tick_params(axis='x', rotation=45)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('../outputs/charts/08_state_volume_vs_leadtime.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 8: State volume vs lead time saved")

# ---- Chart 9: Correlation Heatmap ----
fig, ax = plt.subplots(figsize=(9, 7))
num_cols = ['Lead Time', 'Sales', 'Units', 'Gross Profit', 'Cost']
corr = df[num_cols].corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn', ax=ax,
            mask=mask, linewidths=0.5, vmin=-1, vmax=1,
            annot_kws={'size': 12})
ax.set_title('Correlation Matrix — Numerical Variables', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('../outputs/charts/09_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 9: Correlation heatmap saved")

# ---- Chart 10: Division Performance ----
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

div_avg = df.groupby('Division')['Lead Time'].mean().sort_values()
bars = axes[0].bar(div_avg.index, div_avg.values, color=['#4C72B0','#DD8452','#55A868'], edgecolor='white')
axes[0].set_title('Avg Lead Time by Product Division', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Avg Lead Time (Days)')
for bar, val in zip(bars, div_avg.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, val + 1, f'{val:.0f}d', ha='center', fontsize=12, fontweight='bold')

div_profit = df.groupby('Division')['Gross Profit'].mean().sort_values()
bars = axes[1].bar(div_profit.index, div_profit.values, color=['#4C72B0','#DD8452','#55A868'], edgecolor='white')
axes[1].set_title('Avg Gross Profit by Product Division', fontsize=13, fontweight='bold')
axes[1].set_ylabel('Avg Gross Profit ($)')
for bar, val in zip(bars, div_profit.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, val + 0.05, f'${val:.2f}', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('../outputs/charts/10_division_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print("✓ Chart 10: Division performance saved")

# ============================================================
# STEP 5 — SUMMARY STATISTICS FOR REPORT
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: KEY FINDINGS SUMMARY")
print("=" * 60)

print(f"\n--- DATASET SUMMARY ---")
print(f"Total Orders          : {len(df):,}")
print(f"Unique Routes         : {df['Route_State'].nunique()}")
print(f"Date Range            : {df['Order Date'].min().date()} to {df['Order Date'].max().date()}")
print(f"Overall Avg Lead Time : {df['Lead Time'].mean():.1f} days")
print(f"Overall Delay Rate    : {df['Is_Delayed'].mean()*100:.1f}%")

print(f"\n--- FACTORY RANKINGS (fastest to slowest) ---")
for i, (fac, val) in enumerate(df.groupby('Factory')['Lead Time'].mean().sort_values().items(), 1):
    vol = df['Factory'].value_counts()[fac]
    print(f"  {i}. {fac:25s} | Avg: {val:.0f} days | Volume: {vol:,} shipments")

print(f"\n--- SHIP MODE RANKINGS ---")
for mode, val in df.groupby('Ship Mode')['Lead Time'].mean().sort_values().items():
    delay = df[df['Ship Mode']==mode]['Is_Delayed'].mean()*100
    print(f"  {mode:18s} | Avg: {val:.0f} days | Delay Rate: {delay:.1f}%")

print(f"\n--- REGION RANKINGS ---")
for reg, val in df.groupby('Region')['Lead Time'].mean().sort_values().items():
    vol = df['Region'].value_counts()[reg]
    print(f"  {reg:12s} | Avg: {val:.0f} days | Volume: {vol:,}")

print(f"\n--- TOP 3 MOST EFFICIENT ROUTES ---")
for _, row in route_agg.head(3).iterrows():
    print(f"  {row['Route_State']:50s} | Avg: {row['Avg_Lead_Time']:.0f} days")

print(f"\n--- TOP 3 LEAST EFFICIENT ROUTES ---")
for _, row in route_agg.tail(3).iterrows():
    print(f"  {row['Route_State']:50s} | Avg: {row['Avg_Lead_Time']:.0f} days")

print(f"\n--- TOP 5 STATES BY SHIPMENT VOLUME ---")
for state, vol in df['State/Province'].value_counts().head(5).items():
    avg_lt = df[df['State/Province']==state]['Lead Time'].mean()
    print(f"  {state:20s} | {vol:,} shipments | Avg Lead: {avg_lt:.0f} days")

# Save clean final dataset
df.to_csv('../outputs/reports/cleaned_dataset.csv', index=False)
print("\n✓ Cleaned dataset saved to outputs/reports/cleaned_dataset.csv")

print("\n" + "=" * 60)
print("ALL CHARTS AND REPORTS GENERATED SUCCESSFULLY!")
print("=" * 60)
