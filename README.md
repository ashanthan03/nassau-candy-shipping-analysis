# Nassau Candy Distributor — Shipping Route Efficiency Analysis
## Complete Project by [Your Name] | Unified Mentor Internship

---

## Project Structure

```
nassau_project/
│
├── data/
│   └── Nassau_Candy_Distributor.csv        ← Raw dataset
│
├── notebooks/
│   └── eda_analysis.py                     ← Full EDA script (run this first)
│
├── dashboard/
│   └── app.py                              ← Streamlit dashboard
│
├── outputs/
│   ├── charts/                             ← 10 EDA charts (auto-generated)
│   │   ├── 01_lead_time_distribution.png
│   │   ├── 02_ship_mode_comparison.png
│   │   ├── 03_factory_performance.png
│   │   ├── 04_regional_performance.png
│   │   ├── 05_top_bottom_routes.png
│   │   ├── 06_delay_analysis.png
│   │   ├── 07_time_trends.png
│   │   ├── 08_state_volume_vs_leadtime.png
│   │   ├── 09_correlation_heatmap.png
│   │   └── 10_division_performance.png
│   │
│   └── reports/
│       ├── route_kpis.csv                  ← Route-level KPI table (auto-generated)
│       ├── cleaned_dataset.csv             ← Cleaned data with features (auto-generated)
│       ├── research_paper.md               ← Full research paper
│       └── executive_summary.md            ← Executive summary
│
├── requirements.txt
└── README.md
```

---

## Setup Instructions (One Time Only)

### Step 1: Install Python
Make sure Python 3.9+ is installed. Check with:
```bash
python --version
```

### Step 2: Create a virtual environment (recommended)
```bash
python -m venv nassau_env

# Windows:
nassau_env\Scripts\activate

# Mac/Linux:
source nassau_env/bin/activate
```

### Step 3: Install all dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### STEP A — Run the EDA Analysis (generates all charts)
```bash
cd notebooks
python eda_analysis.py
```
This will:
- Load and clean the dataset
- Engineer all features (Lead Time, Factory, Routes, etc.)
- Generate 10 charts saved in outputs/charts/
- Print all key findings to the console
- Save route_kpis.csv and cleaned_dataset.csv to outputs/reports/

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
5. 📈 Trends & Insights — Time trends, correlations

---

## Deliverables Summary

| Deliverable | Location | Status |
|---|---|---|
| Cleaned Dataset | outputs/reports/cleaned_dataset.csv | ✅ Auto-generated |
| Route KPI Table | outputs/reports/route_kpis.csv | ✅ Auto-generated |
| 10 EDA Charts | outputs/charts/*.png | ✅ Auto-generated |
| Streamlit Dashboard | dashboard/app.py | ✅ Ready to run |
| Research Paper | outputs/reports/research_paper.md | ✅ Complete |
| Executive Summary | outputs/reports/executive_summary.md | ✅ Complete |

---

## Key Findings (Quick Reference)

- **Total Orders:** 10,194 | **Unique Routes:** 196
- **Best Factory:** The Other Factory (Tennessee) — 1,280 days avg
- **Worst Factory:** Sugar Shack (Minnesota) — 1,340 days avg
- **Best Ship Mode:** Standard Class — 1,314 days avg (paradoxically fastest)
- **Best Region:** Gulf — 1,311 days avg
- **Top State (Volume):** California — 2,001 orders
- **Worst Bottleneck:** Sugar Shack → New Jersey — 1,642 days avg
- **Overall Delay Rate:** 42.2% (using median threshold)

---

## Contact
**[Your Name]** | [Your Email] | Unified Mentor Internship
