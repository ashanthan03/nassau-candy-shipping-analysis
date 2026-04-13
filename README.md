# 🍬 Nassau Candy Distributor — Shipping Route Efficiency Analysis

!\[Python](https://img.shields.io/badge/Python-3.12-blue)
!\[Streamlit](https://img.shields.io/badge/Streamlit-1.31-red)
!\[Pandas](https://img.shields.io/badge/Pandas-2.2-green)
!\[Plotly](https://img.shields.io/badge/Plotly-5.19-purple)
!\[Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> \*\*Internship Project | Unified Mentor\*\*



> 🚀 \*\*Live Demo:\*\* https://shipping-route-efficiency.streamlit.app
---

## 📌 Project Overview

Nassau Candy Distributor ships candy products from **5 factories** across the US to customers in **59 states**. This project analyzes **10,194 shipment orders** across **196 unique routes** to identify efficiency bottlenecks, compare shipping modes, and provide data-driven logistics recommendations.

\---

## 🏭 Factories Analyzed

|Factory|Location|Products|
|-|-|-|
|Lot's O' Nuts|Arizona|Wonka Bar (Nutty Crunch, Fudge Mallows, Scrumdiddlyumptious)|
|Wicked Choccy's|Georgia|Wonka Bar (Milk Chocolate, Triple Dazzle Caramel)|
|Sugar Shack|Minnesota|Laffy Taffy, SweeTARTS, Nerds, Fun Dip|
|Secret Factory|Illinois|Everlasting Gobstopper, Wonka Gum|
|The Other Factory|Tennessee|Hair Toffee, Kazookles|

\---

## 📊 Key Findings

* 📦 **10,194 orders** analyzed across **196 factory-to-state routes**
* 🏆 **The Other Factory (TN)** is the fastest — avg 1,280 days lead time
* 🐢 **Sugar Shack to Northeast** routes are the worst bottleneck (1,641-1,642 days)
* 🚚 **Standard Class** is paradoxically faster than First Class and Same Day
* 🌍 **Gulf region** is the most efficient delivery region
* ⚠️ **Washington state** is a high-volume bottleneck (506 orders, 1,361 days avg)

\---

## 🛠 Tech Stack

* **Python 3.12** — Core language
* **Pandas** — Data cleaning and feature engineering
* **Matplotlib / Seaborn** — Static EDA visualizations
* **Plotly** — Interactive charts
* **Streamlit** — Web dashboard
* **Scikit-learn** — Efficiency score normalization

\---

## 📁 Project Structure

```
nassau\_project/
├── data/
├── notebooks/eda\_analysis.py
├── dashboard/app.py
├── outputs/
│   ├── charts/
│   └── reports/
├── screenshots/
├── requirements.txt
└── README.md
```

\---

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/ashanthan03/nassau-candy-shipping-analysis.git
cd nassau-candy-shipping-analysis
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run EDA analysis**

```bash
cd notebooks
python eda\_analysis.py
```

**4. Launch Streamlit dashboard**

```bash
cd dashboard
streamlit run app.py
```

Dashboard opens at: **http://localhost:8501**

\---

## 📈 Dashboard Features

|Tab|Description|
|-|-|
|📊 Route Efficiency|Leaderboard of top/bottom 10 routes|
|🗺 Geographic Map|US heatmap by state|
|🚚 Ship Mode Analysis|Lead time comparison across shipping modes|
|🔍 Route Drill-Down|Order-level timeline for any route|
|📈 Trends \& Insights|Monthly trends and correlations|

\---

## 📸 Dashboard Screenshots

### Route Efficiency Tab

!\[Route Efficiency 1](screenshots/01\_route\_efficiency\_1.png)

!\[Route Efficiency 2](screenshots/01\_route\_efficiency\_2.png)

### Geographic Map Tab

!\[Geographic Map 1](screenshots/02\_geographic\_map\_1.png)

!\[Geographic Map 2](screenshots/02\_geographic\_map\_2.png)

### Ship Mode Analysis Tab

!\[Ship Mode 1](screenshots/03\_shipmode\_1.png)

!\[Ship Mode 2](screenshots/03\_shipmode\_2.png)

### Route Drill-Down Tab

!\[Drill Down 1](screenshots/04\_drilldown\_1.png)

!\[Drill Down 2](screenshots/04\_drilldown\_2.png)

### Trends and Insights Tab

!\[Trends 1](screenshots/05\_trends\_1.png)

!\[Trends 2](screenshots/05\_trends\_2.png)

\---

## 📄 Deliverables

* Research Paper
* Executive Summary
* Interactive Streamlit Dashboard
* Route KPI Table (196 routes)
* 10 EDA Visualization Charts

\---

## 👤 Contact

Akkinapalli Shanthan Kumar | ashanthan03@gmail.com | Unified Mentor Internship

