# Nassau Candy Distributor — Shipping Route Efficiency Analysis

## Complete Project by \[Your Name] | Unified Mentor Internship

\---

## Project Structure

```
nassau\_project/
│
├── data/
│   └── Nassau\_Candy\_Distributor.csv        ← Raw dataset
│
├── notebooks/
│   └── eda\_analysis.py                     ← Full EDA script (run this first)
│
├── dashboard/
│   └── app.py                              ← Streamlit dashboard
│
├── outputs/
│   ├── charts/                             ← 10 EDA charts (auto-generated)
│   │   ├── 01\_lead\_time\_distribution.png
│   │   ├── 02\_ship\_mode\_comparison.png
│   │   ├── 03\_factory\_performance.png
│   │   ├── 04\_regional\_performance.png
│   │   ├── 05\_top\_bottom\_routes.png
│   │   ├── 06\_delay\_analysis.png
│   │   ├── 07\_time\_trends.png
│   │   ├── 08\_state\_volume\_vs\_leadtime.png
│   │   ├── 09\_correlation\_heatmap.png
│   │   └── 10\_division\_performance.png
│   │
│   └── reports/
│       ├── route\_kpis.csv                  ← Route-level KPI table (auto-generated)
│       ├── cleaned\_dataset.csv             ← Cleaned data with features (auto-generated)
│       ├── research\_paper.md               ← Full research paper
│       └── executive\_summary.md            ← Executive summary
│
├── requirements.txt
└── README.md
```

\---

## Setup Instructions (One Time Only)

### Step 1: Install Python

Make sure Python 3.9+ is installed. Check with:

```bash
python --version
```

### Step 2: Create a virtual environment (recommended)

```bash
python -m venv nassau\_env

# Windows:
nassau\_env\\Scripts\\activate

# Mac/Linux:
source nassau\_env/bin/activate
```

### Step 3: Install all dependencies

```bash
pip install -r requirements.txt
```

\---

## Running the Project

### STEP A — Run the EDA Analysis (generates all charts)

```bash
cd notebooks
python eda\_analysis.py
```

This will:

* Load and clean the dataset
* Engineer all features (Lead Time, Factory, Routes, etc.)
* Generate 10 charts saved in outputs/charts/
* Print all key findings to the console
* Save route\_kpis.csv and cleaned\_dataset.csv to outputs/reports/

### STEP B — Launch the Streamlit Dashboard

```bash
cd dashboard
streamlit run app.py
```

This will open the dashboard at: **http://localhost:8501**

The dashboard has 5 tabs:

1. 📊 Route Efficiency — Leaderboard, factory performance
2. 🗺 Geographic Map — US heatmap by state
3. 🚚 Ship Mode Analysis — Comparison across modes
4. 🔍 Route Drill-Down — State + order level detail
5. 📈 Trends \& Insights — Time trends, correlations

\---

## Deliverables Summary

|Deliverable|Location|Status|
|-|-|-|
|Cleaned Dataset|outputs/reports/cleaned\_dataset.csv|✅ Auto-generated|
|Route KPI Table|outputs/reports/route\_kpis.csv|✅ Auto-generated|
|10 EDA Charts|outputs/charts/\*.png|✅ Auto-generated|
|Streamlit Dashboard|dashboard/app.py|✅ Ready to run|
|Research Paper|outputs/reports/research\_paper.md|✅ Complete|
|Executive Summary|outputs/reports/executive\_summary.md|✅ Complete|

\---

## Key Findings (Quick Reference)

* **Total Orders:** 10,194 | **Unique Routes:** 196
* **Best Factory:** The Other Factory (Tennessee) — 1,280 days avg
* **Worst Factory:** Sugar Shack (Minnesota) — 1,340 days avg
* **Best Ship Mode:** Standard Class — 1,314 days avg (paradoxically fastest)
* **Best Region:** Gulf — 1,311 days avg
* **Top State (Volume):** California — 2,001 orders
* **Worst Bottleneck:** Sugar Shack → New Jersey — 1,642 days avg
* **Overall Delay Rate:** 42.2% (using median threshold)

\---

## 📸 Dashboard Screenshots



\### 📊 Route Efficiency

!\[Route Efficiency 1](screenshots/01\_route\_efficiency\_1.png)

!\[Route Efficiency 2](screenshots/01\_route\_efficiency\_2.png)



\### 🗺 Geographic Map

!\[Geographic Map 1](screenshots/02\_geographic\_map\_1.png)

!\[Geographic Map 2](screenshots/02\_geographic\_map\_2.png)



\### 🚚 Ship Mode Analysis

!\[Ship Mode 1](screenshots/03\_shipmode\_1.png)

!\[Ship Mode 2](screenshots/03\_shipmode\_2.png)



\### 🔍 Route Drill-Down

!\[Drill Down 1](screenshots/04\_drilldown\_1.png)

!\[Drill Down 2](screenshots/04\_drilldown\_2.png)



\### 📈 Trends \& Insights

!\[Trends 1](screenshots/05\_trends\_1.png)

!\[Trends 2](screenshots/05\_trends\_2.png)

\---

\## 👤 Contact

\[Akkinapalli Shanthan Kumar] | \[ashanthan03@gmail.com] | Unified Mentor Internship

