# Factory-to-Customer Shipping Route Efficiency Analysis for Nassau Candy Distributor

**Submitted by:** [Your Name]  
**Internship Organization:** Unified Mentor  
**Project:** Nassau Candy Distributor — Logistics Analytics  
**Date:** [Month, Year]

---

## Abstract

This research paper presents a comprehensive data-driven analysis of factory-to-customer shipping route efficiency for Nassau Candy Distributor, a national candy distribution company operating across the United States. Using a dataset of 10,194 shipment orders spanning January 2024 to December 2025, this study investigates shipping lead times across 196 unique factory-to-state routes, five production facilities, four geographic regions, and four shipping modes. Key findings reveal significant performance disparities across routes, a counterintuitive relationship between shipping mode classification and actual delivery speed, and identifiable geographic bottlenecks in northeastern states. The study concludes with actionable recommendations to improve logistics planning, reduce delays, and optimize route-level operations.

---

## 1. Introduction

### 1.1 Background

Nassau Candy Distributor operates as a national distributor shipping products manufactured at five geographically dispersed factories to customers across the United States. The company distributes across three product divisions — Chocolate, Sugar, and Other — comprising 15 distinct candy products. Despite having rich transactional data, the organization lacked a systematic, route-level understanding of its shipping performance.

Efficient logistics is critical to the company's competitiveness. Delayed shipments increase operational costs, erode customer satisfaction, and reduce the scalability of distribution operations. Without data-driven visibility into route-level performance, logistics optimization remains largely reactive.

### 1.2 Problem Statement

This study addresses four specific operational gaps:

1. Which factory-to-customer routes are consistently efficient, and which experience frequent delays?
2. How does shipping performance vary across regions, states, and shipping modes?
3. Where do geographic bottlenecks exist in the distribution network?
4. What operational recommendations can be drawn from route-level efficiency intelligence?

### 1.3 Scope

The analysis is scoped to domestic US shipments from five factories to customers in 59 states and territories. The dataset contains 10,194 orders, 18 fields per record, and zero missing values. The primary metric throughout is **Shipping Lead Time**, defined as the number of days between an order date and its corresponding shipment date.

---

## 2. Dataset Description

### 2.1 Data Source

The dataset was provided as a single CSV file containing transactional shipment records. Each row represents one order line item.

### 2.2 Field Definitions

| Field | Description |
|---|---|
| Row ID | Unique row identifier |
| Order ID | Unique order identifier |
| Order Date | Date the order was placed |
| Ship Date | Date the order was shipped |
| Ship Mode | Shipping classification (Standard, Second, First, Same Day) |
| Customer ID | Unique customer identifier |
| Country/Region | Country of customer |
| City | Customer city |
| State/Province | Customer state |
| Postal Code | Customer postal code |
| Division | Product division (Chocolate, Sugar, Other) |
| Region | Geographic region (Atlantic, Gulf, Interior, Pacific) |
| Product ID | Unique product identifier |
| Product Name | Full product name |
| Sales | Total sales value of the order |
| Units | Total units ordered |
| Gross Profit | Sales minus manufacturing cost |
| Cost | Manufacturing cost |

### 2.3 Dataset Quality

The dataset was found to be remarkably clean with **zero missing values** across all 18 columns and **zero invalid lead times**. The format of date fields uses DD-MM-YYYY convention. Order dates span January 2024 through December 2025, while ship dates extend into 2026–2030, resulting in lead times ranging from 904 to 1,642 days. As this is a synthetic training dataset designed for analytical purposes, these absolute lead time values are acknowledged as non-representative of real-world candy distribution timelines; however, the relative differences across routes, factories, and shipping modes are meaningful and form the basis of all comparative analysis in this paper.

### 2.4 Factory-Product Mapping

Five factories supply the product portfolio. Each factory is associated with specific products as follows:

| Factory | Location | Products |
|---|---|---|
| Lot's O' Nuts | Arizona | Wonka Bar (Nutty Crunch, Fudge Mallows, Scrumdiddlyumptious) |
| Wicked Choccy's | Georgia | Wonka Bar (Milk Chocolate, Triple Dazzle Caramel) |
| Sugar Shack | Minnesota/ND border | Laffy Taffy, SweeTARTS, Nerds, Fun Dip, Fizzy Lifting Drinks |
| Secret Factory | Illinois | Everlasting Gobstopper, Lickable Wallpaper, Wonka Gum |
| The Other Factory | Tennessee | Hair Toffee, Kazookles |

---

## 3. Methodology

### 3.1 Data Cleaning and Validation

The following validation steps were performed:

- Date columns were parsed using `dayfirst=True` to correctly interpret the DD-MM-YYYY format
- Shipping Lead Time was computed as `Ship Date − Order Date` in calendar days
- All 10,194 rows were retained after validation (no records removed)
- Categorical fields (Ship Mode, Region, State) were inspected for consistency
- A factory assignment column was added by mapping each Product Name to its corresponding factory

### 3.2 Feature Engineering

Key derived features created for analysis:

- **Lead Time (days):** Primary metric; computed from date difference
- **Factory:** Derived from product-factory mapping
- **Route_by_State:** Concatenation of Factory and State (e.g., "Lot's O' Nuts → California")
- **Route_by_Region:** Concatenation of Factory and Region
- **Is_Delayed:** Binary flag — 1 if Lead Time exceeds the dataset median (1,274 days), 0 otherwise
- **Efficiency_Score:** Min-max normalized inverse of average lead time per route (1.0 = fastest, 0.0 = slowest)
- **Order_Year / Order_Month:** Temporal decomposition for trend analysis

### 3.3 Delay Definition

Since the dataset is synthetic with non-standard absolute lead times, a median-based delay threshold of **1,274 days** was used rather than an arbitrary fixed value. Shipments exceeding this threshold are classified as delayed. This approach captures the top ~42% of slowest shipments as the "delayed" cohort.

### 3.4 Route Aggregation

Each unique route (Factory → State combination) was aggregated to compute:
- Total shipments, average and standard deviation of lead time
- Delay rate (proportion of delayed shipments)
- Total sales, average gross profit
- Efficiency Score (normalized)

### 3.5 Visualization and Analysis

Ten visualization charts were produced covering lead time distributions, factory and ship mode comparisons, regional performance, top/bottom route rankings, delay analysis, temporal trends, state-level volume analysis, and correlation mapping. An interactive Streamlit web dashboard was built to provide stakeholders with filterable, real-time analytics.

---

## 4. Exploratory Data Analysis

### 4.1 Lead Time Distribution

The distribution of shipping lead times is markedly **bimodal**, with a large cluster concentrated around 1,271–1,274 days and a second cluster concentrated around 1,638–1,642 days. This bimodal pattern suggests two distinct shipping cohorts within the data — a fast cohort and a slow cohort — with a gap of approximately 364 days between them. The mean lead time is 1,320.8 days with a standard deviation of 262.4 days. The relatively high standard deviation relative to the mean reflects this bimodal structure.

| Statistic | Value (days) |
|---|---|
| Minimum | 904 |
| 25th Percentile | 1,271 |
| Median | 1,274 |
| Mean | 1,321 |
| 75th Percentile | 1,638 |
| Maximum | 1,642 |

### 4.2 Factory Volume and Performance

Lot's O' Nuts and Wicked Choccy's together account for 96.6% of all shipments (9,844 out of 10,194), making them the dominant factories in the distribution network. The remaining three factories — Sugar Shack, Secret Factory, and The Other Factory — have very low shipment volumes (33, 217, and 100 orders respectively), meaning their route-level averages may be influenced by small sample sizes.

| Factory | Avg Lead Time | Shipments | % of Total |
|---|---|---|---|
| The Other Factory | 1,280 days | 100 | 1.0% |
| Wicked Choccy's | 1,321 days | 4,152 | 40.7% |
| Lot's O' Nuts | 1,321 days | 5,692 | 55.8% |
| Secret Factory | 1,322 days | 217 | 2.1% |
| Sugar Shack | 1,340 days | 33 | 0.3% |

The Other Factory in Tennessee achieves the best average lead time at 1,280 days, outperforming all other facilities despite its low volume. Sugar Shack in Minnesota is the slowest at 1,340 days average — 60 days more than the best performer.

### 4.3 Ship Mode Analysis

A counterintuitive pattern emerges in the ship mode data: Standard Class shipments have the **lowest** average lead time (1,314 days), while First Class and Same Day shipments are slower:

| Ship Mode | Avg Lead Time | Delay Rate | Volume |
|---|---|---|---|
| Standard Class | 1,314 days | 46.8% | 6,120 |
| Second Class | 1,324 days | 34.0% | 1,979 |
| Same Day | 1,333 days | 34.4% | 547 |
| First Class | 1,338 days | 37.2% | 1,548 |

This paradox — where Standard Class leads fastest — suggests that shipping mode classification may not reflect actual transit priority in this dataset. Standard Class handles the largest volume (60% of all orders) and may benefit from better-optimized routes or different order processing pipelines.

### 4.4 Regional Performance

The Gulf region achieves the lowest average lead time at 1,311 days, while the Atlantic, Pacific, and Interior regions are closely clustered at 1,322–1,323 days.

| Region | Avg Lead Time | Volume |
|---|---|---|
| Gulf | 1,311 days | 1,620 |
| Pacific | 1,322 days | 3,253 |
| Atlantic | 1,323 days | 2,986 |
| Interior | 1,323 days | 2,335 |

### 4.5 Top 10 Most Efficient Routes

| Route | Avg Lead Time | Shipments |
|---|---|---|
| Secret Factory → New Mexico | 906 days | 2 |
| Secret Factory → Nebraska | 906 days | 1 |
| The Other Factory → Louisiana | 907 days | 1 |
| The Other Factory → Connecticut | 907.5 days | 2 |
| Secret Factory → Mississippi | 908 days | 1 |
| Wicked Choccy's → Maine | 908 days | 2 |
| Secret Factory → Louisiana | 908.5 days | 2 |
| Secret Factory → Delaware | 909 days | 1 |
| Secret Factory → South Carolina | 909 days | 1 |
| Secret Factory → Minnesota | 909 days | 1 |

Note: Most top-efficient routes have very low shipment volumes (1–2 orders), which limits the statistical reliability of these averages. Among high-volume routes, the most efficient routes originate from Lot's O' Nuts and Wicked Choccy's to southeastern and Gulf states.

### 4.6 Bottom 10 Least Efficient Routes

| Route | Avg Lead Time | Shipments |
|---|---|---|
| Sugar Shack → New Jersey | 1,642 days | 1 |
| Sugar Shack → Connecticut | 1,641 days | 1 |
| Secret Factory → New Hampshire | 1,641 days | 1 |
| Wicked Choccy's → West Virginia | 1,639 days | 2 |
| Lot's O' Nuts → North Dakota | 1,638 days | 5 |
| Secret Factory → Connecticut | 1,638 days | 1 |
| Sugar Shack → California | 1,638 days | 1 |
| Sugar Shack → Washington | 1,638 days | 1 |
| The Other Factory → Nevada | 1,638 days | 1 |
| Secret Factory → Kentucky | 1,637.5 days | 2 |

The least efficient routes are concentrated in routes where factories ship to geographically distant or directionally opposite states (e.g., Sugar Shack in Minnesota shipping to northeastern coastal states like NJ and CT).

### 4.7 Geographic Bottleneck Analysis

California (2,001 orders), New York (1,128), and Texas (985) are the three highest-volume states. Washington state shows the highest average lead time among top-volume states at 1,361 days, making it a notable operational bottleneck given its combination of high volume and poor lead time performance.

| State | Volume | Avg Lead Time |
|---|---|---|
| California | 2,001 | 1,318 days |
| New York | 1,128 | 1,324 days |
| Texas | 985 | 1,310 days |
| Pennsylvania | 587 | 1,324 days |
| Washington | 506 | 1,361 days |

### 4.8 Division-Level Analysis

The three product divisions show slight performance variation:

| Division | Avg Lead Time | Avg Gross Profit |
|---|---|---|
| Chocolate | ~1,321 days | Higher |
| Other | ~1,322 days | Medium |
| Sugar | ~1,340 days | Lower |

The Chocolate division benefits from being produced by the two largest, best-optimized factories (Lot's O' Nuts and Wicked Choccy's), which may explain its slightly faster average lead time.

### 4.9 Correlation Analysis

Correlation analysis of numerical variables reveals:

- **Sales and Gross Profit** show a strong positive correlation (~0.98), as expected
- **Sales and Units** are moderately positively correlated (~0.75)
- **Lead Time** shows near-zero correlation with all financial variables (Sales, Profit, Cost), confirming that order value does not influence shipping speed — a finding that may indicate no expedited handling is applied to high-value orders

---

## 5. Key Findings

1. **The distribution network is dominated by two factories.** Lot's O' Nuts (55.8%) and Wicked Choccy's (40.7%) together handle 96.6% of all shipments, creating a significant concentration risk in the supply chain.

2. **Standard Class shipping is paradoxically the fastest mode.** Despite being the lowest-priority shipping classification, Standard Class achieves the lowest average lead time at 1,314 days versus 1,338 days for First Class. This warrants investigation into whether premium shipping modes are delivering value for money.

3. **The Other Factory in Tennessee is the best-performing facility.** At 1,280 days average lead time, it outperforms all other factories by at least 41 days, despite having the second-lowest shipment volume.

4. **Sugar Shack routes to the Northeast are the network's worst bottleneck.** Sugar Shack in Minnesota shipping to New Jersey (1,642 days), Connecticut (1,641 days), and New Hampshire (1,641 days) represents the most extreme lead time inefficiencies — likely driven by geographic distance and potentially routing constraints.

5. **The Gulf region is the most efficient geographic region.** Gulf-bound shipments average 1,311 days, 12 days faster than the next best region.

6. **High order value does not correlate with faster shipping.** The near-zero correlation between Lead Time and Sales/Profit suggests no premium handling is applied to high-value orders, representing a potential service improvement opportunity.

7. **Washington state is a high-volume bottleneck.** With 506 orders and an average lead time of 1,361 days — 43 days above the overall average — Washington represents a priority target for logistics optimization.

---

## 6. Recommendations

### 6.1 Investigate and Address the Ship Mode Paradox
Conduct an internal audit of why Standard Class shipments outperform First Class and Same Day modes. If premium modes are not delivering faster transit, the company should either restructure shipping contracts with carriers or reclassify orders to avoid unnecessarily high shipping costs.

### 6.2 Prioritize Route Optimization for Sugar Shack → Northeast Routes
The routes from Sugar Shack (Minnesota) to northeastern states (NJ, CT, NH) are the worst performers in the network. The company should evaluate whether regional fulfillment partnerships, inventory repositioning, or carrier renegotiation could reduce these lead times.

### 6.3 Address the Washington State Bottleneck
Washington state is a high-volume state (506 orders) with significantly above-average lead times (1,361 days). Dedicated carrier agreements or routing adjustments for Pacific Northwest delivery could yield measurable improvements.

### 6.4 Reduce Supply Chain Concentration Risk
With 96.6% of orders flowing through just two factories, any operational disruption at Lot's O' Nuts or Wicked Choccy's would cripple the distribution network. The company should explore capacity expansion at The Other Factory (which has the best lead time performance) and Secret Factory.

### 6.5 Implement Lead Time-Based SLA Tiers
Using the route efficiency scores developed in this analysis, the company should establish service level agreements (SLAs) at the route level. Routes with efficiency scores above 0.8 can be held to tighter delivery commitments, while routes below 0.3 should be flagged for operational review.

### 6.6 Apply Value-Based Shipping Prioritization
Since high-value orders currently receive no shipping speed advantage, the company should consider implementing tiered handling where orders above a sales threshold (e.g., $50+) are automatically upgraded to a faster routing option.

---

## 7. Conclusion

This analysis establishes a comprehensive, data-driven understanding of shipping route efficiency for Nassau Candy Distributor. By transforming 10,194 order records into route-level operational intelligence across 196 factory-to-state routes, this study identifies the key performance drivers and bottlenecks within the company's nationwide distribution network.

The findings reveal that while the company's two primary factories perform comparably on average, significant route-level variation exists that is currently invisible to logistics planners. The counterintuitive ship mode performance paradox, the geographic concentration of poor-performing routes in the Northeast, and the outsized influence of Washington state as a high-volume bottleneck all represent actionable opportunities for operational improvement.

The interactive Streamlit dashboard developed as part of this project provides ongoing visibility into these metrics, enabling logistics teams to monitor route performance in real time, apply targeted filters, and drill down to the order level for root cause analysis. With these tools in place, Nassau Candy Distributor is well-positioned to transition from reactive to proactive logistics management.

---

## References

- Nassau Candy Distributor Dataset (provided by Unified Mentor)
- McKinsey & Company: *Supply Chain Efficiency in Consumer Goods Distribution*, 2023
- Pandas Documentation: https://pandas.pydata.org/docs/
- Streamlit Documentation: https://docs.streamlit.io/
- Plotly Express Documentation: https://plotly.com/python/plotly-express/

---

## Appendix A: KPI Definitions

| KPI | Formula | Description |
|---|---|---|
| Shipping Lead Time | Ship Date − Order Date | Days from order to shipment |
| Average Lead Time | Mean(Lead Time) per route | Route-level central tendency |
| Route Volume | COUNT(orders) per route | Number of shipments per route |
| Delay Frequency | % of orders > Threshold | Proportion of delayed shipments |
| Efficiency Score | 1 − MinMaxNorm(Avg Lead Time) | 1=fastest, 0=slowest |

## Appendix B: Factory Coordinates

| Factory | Latitude | Longitude | State |
|---|---|---|---|
| Lot's O' Nuts | 32.881893 | -111.768036 | Arizona |
| Wicked Choccy's | 32.076176 | -81.088371 | Georgia |
| Sugar Shack | 48.11914 | -96.18115 | MN/ND border |
| Secret Factory | 41.446333 | -90.565487 | Illinois |
| The Other Factory | 35.1175 | -89.971107 | Tennessee |
