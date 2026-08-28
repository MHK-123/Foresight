# PROJECT FORESIGHT: RETAIL DEMAND FORECASTING & INVENTORY RISK INTELLIGENCE

**Final Internship Project Report**  
**Client:** NorthBay Living  
**Role:** Data Science & Analytics Intern (Zidio Development Internship)  
**Author:** MHK  
**Repository:** [https://github.com/MHK-123/Foresight](https://github.com/MHK-123/Foresight)  
**Date:** August 2026  

---

## 1. Title Page & Executive Summary

* **Project Title:** FORESIGHT — Demand & Inventory Intelligence Platform
* **Client Organization:** NorthBay Living (Multi-format retail chain with 30 store locations across 4 major metropolitan cities)
* **Project Scope:** Multi-echelon demand forecasting, synthetic contamination handling, explainable inventory risk scoring, and interactive decision-support tooling.
* **Core Achievement:** Developed a production-grade LightGBM Gradient Boosted Decision Tree forecasting model achieving **42.16% Out-of-Sample WAPE** (-11.3% error reduction over baseline) and **1.183 RMSE** (-20.3% error reduction) across 8.513M daily store-SKU observations. Built an automated risk scoring engine that identified **Rs. 1.78 Billion in trapped overstock working capital** and **5,209 stockout deficit positions** with **100.0% validation recall** on known inventory anomalies.

---

## 2. Project Overview

NorthBay Living operates a retail network spanning 30 physical stores across 4 store formats (Supermarket, Hypermarket, Express, Gourmet) and multiple distribution channels (In-Store, Online Delivery, BOPIS, Wholesale). Managing 5,000 active SKUs across 12 distinct merchandise categories, the enterprise faced severe inventory imbalances: simultaneous chronic stockouts on high-velocity essentials and multi-million rupee capital lockup in stagnant, slow-moving items.

Project FORESIGHT was commissioned to replace rudimentary historical heuristics with an end-to-end, machine-learning-driven inventory intelligence system. The platform unifies granular transaction logs, promotional calendars, pricing elasticity, and store metadata into a unified predictive engine and executive decision-support interface.

---

## 3. Business Problem & Objectives

### 3.1 Business Pain Points
1. **Lost Revenue from Out-of-Stock (OOS) Events:** High-velocity staple items frequently experienced zero-stock conditions, leading to uncaptured demand, customer dissatisfaction, and revenue leakage.
2. **Excess Working Capital in Stagnant Inventory:** Millions of rupees were locked in slow-moving merchandise exceeding 120+ days of supply, inflating inventory holding costs and risk of obsolescence.
3. **Flawed Historical Demand Signals:** Past out-of-stock periods recorded zero sales, distorting traditional moving averages and leading to systematic under-forecasting and chronic under-replenishment.
4. **Lack of Explainable Actionability:** Store and inventory managers lacked transparent, priority-ranked purchase order recommendations and cross-store reallocation visibility.

### 3.2 Key Project Objectives
* **Build an Accurate ML Demand Forecaster:** Train and validate multi-horizon regression models that significantly outperform baseline heuristics (SMA, Seasonal Lags) across all 30 stores and 5,000 SKUs.
* **Preserve Temporal Integrity:** Prevent all forms of data leakage across chronological train/validation/test splits.
* **Develop an Explainable Risk Engine:** Calculate forward demand horizons (7, 14, 30 days), dynamically evaluate Days of Supply (DOS), and classify all 26,408 store-SKU positions into deterministic risk tiers.
* **Deliver an Operational Dashboard:** Provide supply chain planners with interactive visualization, what-if scenario simulation, priority action worklists, and cross-store transfer intelligence.

---

## 4. Dataset & Data Architecture

The project analyzed 4 years of retail operations from **January 1, 2022 to December 31, 2025** comprising 9,945,396 raw transaction records.

### 4.1 Enterprise Data Tables & Audit Statistics

| Dataset Name | Record Count | Column Count | Primary Key / Grain | Key Attributes |
| :--- | :---: | :---: | :--- | :--- |
| `transactions_clean.parquet` | 9,945,396 | 13 | `transaction_id`, `date` | Transaction date, Store ID, SKU ID, Quantity, Unit Price, Total Amount, Discount Applied, Promotion ID, Channel, Payment Method |
| `inventory_clean.parquet` | 26,408 | 7 | `store_id` $\times$ `sku_id` | Store ID, SKU ID, Current Stock on Hand, Reorder Point, Safety Stock Buffer, Last Restock Date |
| `products_clean.parquet` | 5,000 | 7 | `sku_id` | SKU ID, Product Name, Category, Subcategory, Brand, Cost Price (PKR), Retail Price (PKR) |
| `stores_clean.parquet` | 30 | 6 | `store_id` | Store ID, Store Name, Store Type, City, Regional Tier, Size SqFt |
| `promotions_clean.parquet` | 730 | 7 | `promo_id` | Promotion ID, Promo Name, Promo Type, Discount %, Start Date, End Date, Target Category |
| `sku_inventory_flags.parquet` | 11,649 | 4 | `store_id` $\times$ `sku_id` | Store ID, SKU ID, Ground-Truth Defect Flag (`STOCKOUT_INJECTED`, `SLOW_MOVER_INJECTED`), Injection Timestamp |

### 4.2 Entity Relational Model (ERD)

```text
  +----------------------+             +--------------------------+
  |    STORES (30)       |             |      PRODUCTS (5,000)    |
  +----------------------+             +--------------------------+
  | PK  store_id         |             | PK  sku_id               |
  |     store_name       |             |     sku_name             |
  |     store_type       |             |     category             |
  |     city             |             |     cost_price           |
  |     size_sqft        |             |     retail_price         |
  +----------+-----------+             +------------+-------------+
             |                                      |
             | 1:N                                  | 1:N
             |          +--------------------+      |
             +--------->| TRANSACTIONS       |<-----+
             |          | (9.945M Rows)      |
             |          +--------------------+
             |          | PK  transaction_id |
             |          | FK  store_id       |
             |          | FK  sku_id         |
             |          |     date           |
             |          |     quantity       |
             |          |     total_amount   |
             |          |     channel        |
             |          +--------------------+
             |                                      |
             | 1:N                                  | 1:N
             +--------->+--------------------+<-----+
                        | INVENTORY (26,408) |
                        +--------------------+
                        | PK  store_id       |
                        | PK  sku_id         |
                        |     stock_on_hand  |
                        |     safety_stock   |
                        |     reorder_point  |
                        |     last_restock   |
                        +--------------------+
```

---

## 5. Technology Stack

* **Data Processing & High-Performance Analytics:** Python 3.13, `Polars` (zero-copy multithreaded engine handling 8.5M+ daily aggregations), `Pandas`, `NumPy`, `PyArrow`.
* **Machine Learning & Statistical Modeling:** `LightGBM` (Gradient Boosted Decision Trees), `scikit-learn` (Time-series split evaluation and feature pipelines), `Joblib`.
* **Visualization & Reporting:** `Plotly Express & Graph Objects`, `Matplotlib`, `Seaborn`, `ReportLab` (PDF Report Compilation).
* **Enterprise Web Application:** `Streamlit` (Multi-view responsive decision dashboard, custom BaseWeb popover styling, CSS design tokens).
* **Version Control & Repository Management:** `Git`, `GitHub`.

---

## 6. End-to-End System Architecture

```text
  RAW DATA LAKE (9.95M Rows)
     ├── Transactions / Sales
     ├── Store & SKU Metadata
     └── Inventory Status Logs
                │
                ▼
  STEP 2: DATA CLEANING & RECONCILIATION
     ├── Schema Casting & Type Enforcement
     ├── Timestamp Normalization (2022-2025)
     └── Isolation of Synthetic Defect Flags
                │
                ▼
  STEP 4: TIME-SERIES FEATURE ENGINEERING (8.513M x 57 Matrix)
     ├── Calendar & Fourier Cycles (Day of week, Month, Holiday flags)
     ├── Price Elasticity & Promotional Discount Ratios
     ├── Rolling Aggregations (7d, 14d, 28d, 60d Means, Std, Min, Max)
     └── Autoregressive Lags (Lag-7, Lag-14, Lag-21, Lag-28)
                │
                ▼
  STEP 6: TEMPORAL MACHINE LEARNING PIPELINE
     ├── Train Split (2022-01-01 to 2024-12-31 | 6.38M Rows)
     ├── Validation Split (2025-01-01 to 2025-06-30 | 1.07M Rows)
     └── Test Split (2025-07-01 to 2025-12-31 | 1.07M Rows)
                │
                ▼
  STEP 7: LIGHTGBM MODEL EVALUATION & DIAGNOSIS
     ├── Out-of-Sample Test WAPE: 42.16%
     ├── Test RMSE: 1.183 | Network Bias: -0.01%
     └── Top-Bestseller WAPE: 20.75%
                │
                ▼
  STEP 8: EXPLAINABLE RISK SCORING ENGINE (26,408 Nodes)
     ├── Forward Demand Horizons (7d, 14d, 30d Projections)
     ├── Dynamic Days-of-Supply (DOS = Stock / Forecasted Velocity)
     ├── Lead-Time Breach Detection (Stock < Lead-Time Demand + Safety Buffer)
     └── Stagnation Scoring (DOS > 120d + Stale Restock > 90d)
                │
                ▼
  STEP 9: STREAMLIT INTELLIGENCE PLATFORM (app.py)
     ├── 1. Executive Health & Working Capital Overview
     ├── 2. Stockout Risk Deficit Worklists
     ├── 3. Overstock & Trapped Capital Optimizer
     ├── 4. Interactive Actual vs. Forecast Explorer
     ├── 5. SKU & Store Inventory Explorer (CSV Export)
     ├── 6. Priority Action Center (Emergency POs & Store Transfers)
     ├── 7. What-If Supply Chain Simulator
     └── 8. Data-Grounded Intelligence Assistant (AI)
```

---

## 7. Data Cleaning & Preparation

1. **Transaction De-duplication & Type Casting:** Audited 9.945M transaction records. Ensured zero orphan records by verifying strict referential integrity against store and product dimension tables.
2. **Handling Synthetic Contamination:** Identified 11,649 injected ground-truth defect records (`sku_inventory_flags.parquet`). To prevent data leakage, these flags were strictly quarantined and excluded from all feature engineering and model training pipelines.
3. **Daily Store-SKU Aggregation:** Transformed discrete transaction logs into a continuous daily time-series grid of 8,513,440 store-SKU-date observations, filling non-sale operating days with zero volume.

---

## 8. Exploratory Data Analysis (EDA)

Key business insights discovered during Step 3 EDA:

1. **Network Growth & Macro Trends:** Network sales grew steadily at approximately **+6.0% YoY** from 2022 through 2025, with peak volumes occurring during Q4 holiday seasons.
2. **Pareto Demand Concentration:** The top **20% of SKUs accounted for 58.8% of total sales volume**, demonstrating heavy revenue reliance on a core set of bestseller products.
3. **Category Volume Distribution:** *Grocery* (24.1%) and *Dairy & Bakery* (18.4%) constituted the highest sales volume, while *Electronics & Accessories* and *Home & Kitchen* carried the highest capital exposure per unit.
4. **Day-of-Week Seasonality:** Sales exhibited substantial weekend surges (+32.4% on Saturday and Sunday compared to weekday averages).
5. **Promotional Responsiveness:** Buy-One-Get-One (BOGO) promotions generated the highest volume lift (+41.2%), followed by percentage discounts (+23.8%).

---

## 9. Baseline Forecasting Benchmarks

To establish rigorous performance benchmarks before developing machine learning models, 5 statistical baselines were evaluated on the exact chronological test split (H2 2025: 1,066,548 observations):

| Baseline Model | Methodology | Test WAPE (%) | Test RMSE | Test MAE | Test Bias (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Historical Mean** | Global store-SKU average daily demand | 68.42% | 2.140 | 1.482 | +4.12% |
| **Lag-1 Persistence** | Yesterday's actual sales volume | 58.19% | 1.812 | 1.261 | -0.15% |
| **Lag-7 Seasonal** | Same day of previous week | 52.34% | 1.624 | 1.134 | -0.08% |
| **7-Day Rolling SMA** | Trailing 7-day simple moving average | 49.88% | 1.542 | 1.081 | -0.11% |
| **28-Day Rolling SMA** | Trailing 28-day simple moving average | **47.54%** | **1.485** | **1.030** | **-0.04%** |

*Key Takeaway:* The strongest statistical baseline was the **28-Day Rolling SMA (47.54% WAPE, 1.485 RMSE)**.

---

## 10. Machine Learning Forecasting Models

### 10.1 Feature Engineering (52 Predictor Features)
Constructed 52 rolling, lag, and calendar features across 8.513M rows:
* **Autoregressive Lags:** Lag-7, Lag-14, Lag-21, Lag-28 sales quantities.
* **Rolling Window Statistics:** 7d, 14d, 28d, 60d Rolling Means, Rolling Standard Deviations, Rolling Min, and Rolling Max.
* **Promotional & Pricing Features:** Active discount percentage, promotion type indicator, price gap ratio against category average.
* **Calendar & Cyclical Signals:** Day of week (sine/cosine encoded), Day of month, Month of year, Is_Weekend flag, Is_Holiday flag.
* **Entity Encodings:** Target-encoded Store Format, Category, and City historical sales velocity.

### 10.2 Model Training Setup
* **Algorithm:** LightGBM Regressor (Histogram-based GBDT)
* **Chronological Temporal Split:**
  * **Train Set:** 2022-01-01 to 2024-12-31 (6,378,000 rows | 3 years)
  * **Validation Set:** 2025-01-01 to 2025-06-30 (1,068,892 rows | H1 2025)
  * **Test Set:** 2025-07-01 to 2025-12-31 (1,066,548 rows | H2 2025)
* **Hyperparameters (Model 2 - Production):** `n_estimators=70`, `learning_rate=0.08`, `num_leaves=63`, `max_depth=8`, `colsample_bytree=0.8`, `subsample=0.8`, `objective='regression'` (L2 loss).

---

## 11. Model Evaluation & Diagnosis

### 11.1 Test Set Benchmark Comparison

| Model Architecture | Test WAPE (%) | Test RMSE | Test MAE | Test Bias (%) | Relative WAPE Gain | Relative RMSE Gain |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 28-Day Rolling SMA Baseline | 47.54% | 1.485 | 1.030 | -0.04% | Baseline | Baseline |
| LightGBM Model 1 (L1 Loss / Hubers) | 43.82% | 1.246 | 0.949 | -0.84% | +7.8% | +16.1% |
| **LightGBM Model 2 (L2 Loss - Production)** | **42.16%** | **1.183** | **0.928** | **-0.01%** | **+11.3%** | **+20.3%** |

### 11.2 Segmented Performance Diagnostics
* **High-Velocity Bestsellers (Top 20% SKUs):** Achieved **20.75% WAPE**, providing highly dependable replenishment accuracy for core revenue generators.
* **Low-Velocity / Intermittent Items:** Achieved **54.30% WAPE**, reflecting Poisson-like intermittent demand dynamics.
* **Network Bias Integrity:** The model recorded an overall network bias of **-0.01%**, demonstrating zero structural over-forecasting or under-forecasting bias.
* **Feature Importance:** Rolling 28-day mean (`sales_roll_mean_28`), Lag-7 sales (`sales_lag_7`), and active promotional discount (`discount_pct`) emerged as the top 3 demand drivers.

---

## 12. Inventory Risk Scoring Engine

The Step 8 risk engine scored all **26,408 active store-SKU inventory positions** using the production LightGBM demand forecasts.

### 12.1 Explainable Classification Logic
1. **Critical Stockout:** Physical Stock = 0 units. (Lost sales occurring immediately).
2. **High Stockout Risk:** $0 < \text{Stock} < \text{Safety Stock Buffer}$.
3. **Medium Stockout Risk:** $\text{Safety Stock} \le \text{Stock} < (\text{Forecasted 7-Day Lead Demand} + \text{Safety Buffer})$.
4. **Healthy / Optimal:** $7 \le \text{Days of Supply (DOS)} \le 45$ days and $\text{Stock} < 2.5 \times \text{Reorder Point}$.
5. **Medium Overstock:** $45 < \text{DOS} \le 90$ days.
6. **High Overstock:** $90 < \text{DOS} \le 120$ days or $\text{Stock} \ge 2.5 \times \text{Reorder Point}$.
7. **Critical Dead Stock:** $\text{DOS} > 120$ days and $\text{Days Since Last Restock} > 90$ days.

### 12.2 Enterprise Inventory Audit Results

| Risk Classification Tier | Node Count | % of Network | Total Physical Units | Trapped Capital (Cost PKR) | Recommended Operational Action |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **CRITICAL_STOCKOUT** | 4,239 | 16.05% | 0 | Rs. 0.00 | Emergency Expedited Purchase Order |
| **HIGH_STOCKOUT_RISK** | 970 | 3.67% | 48,192 | Rs. 19,420,110 | Urgent Reorder PO to Restore Safety Buffer |
| **MEDIUM_STOCKOUT_RISK** | 764 | 2.89% | 61,208 | Rs. 24,810,400 | Standard Cycle Replenishment PO |
| **HEALTHY_OPTIMAL** | 2,444 | 9.25% | 137,497 | Rs. 70,781,417 | Maintain Routine Scheduled Monitoring |
| **MEDIUM_OVERSTOCK** | 1,899 | 7.19% | 298,401 | Rs. 122,110,950 | Reduce Next Cycle Purchase Order Quantity |
| **HIGH_OVERSTOCK** | 6,708 | 25.40% | 1,421,801 | Rs. 598,340,120 | Freeze Purchase Orders & Reallocate Stock |
| **CRITICAL_OVERSTOCK** | 9,384 | 35.53% | 2,421,800 | Rs. 1,057,994,569 | Execute Clearance Markdowns (25%-35% Off) |
| **TOTAL NETWORK** | **26,408** | **100.0%** | **4,388,899** | **Rs. 1,849,231,166** | **Network Working Capital Optimization** |

### 12.3 Ground-Truth Defect Validation
* **Stockout Defect Injection Recall:** **100.0%** ($2,703 / 2,703$ injected anomalies successfully detected).
* **Slow Mover Injection Recall:** **100.0%** ($8,946 / 8,946$ injected anomalies successfully detected).

---

## 13. Streamlit Decision Platform

The FORESIGHT interactive web application (`app.py`) provides supply chain executives and inventory planners with 8 operational modules:

1. **Executive Overview:** High-level KPI scorecards, working capital exposure charts, and department-level summaries.
2. **Stockout Risk:** Real-time visibility into zero-stock positions, lost revenue risk, and prescriptive PO recommendations.
3. **Overstock / Slow Movers:** Identifies Rs. 1.78B in trapped capital, staleness scatter plots, and clearance markdown candidates.
4. **Demand Forecast:** Interactive test-period time series visualizer comparing actual sales against LightGBM predictions and baselines.
5. **Inventory Explorer:** Searchable, filterable 26,408-row worklist with one-click CSV export.
6. **Priority Action Center:** Categorized operational worklists for immediate replenishment, stockout prevention, clearance sales, and automated inter-store stock transfers.
7. **What-If Inventory Simulator:** Interactive sandbox allowing users to simulate vendor lead times, safety stocks, and demand velocity.
8. **Intelligence Assistant:** Natural-language query interface grounded in verified project outputs, featuring single-item explainability.

---

## 14. Key Results & Business Insights

1. **Rs. 1.78 Billion Working Capital Recovery Potential:** Overstock positions tie up 96.1% of NorthBay Living's working capital. Implementing clearance markdowns and freezing POs on dead stock can unlock hundreds of millions of rupees in cash flow.
2. **5,209 Deficit Positions Protected:** Preemptive replenishment orders based on LightGBM lead-time projections eliminate lost sales across 19.7% of the network.
3. **Inter-Store Balancing Opportunities:** The system identified hundreds of cross-store inventory matches where one store is out of stock while a neighboring store carries $>90$ days of excess stock for the exact same SKU.

---

## 15. Challenges & Limitations

* **Intermittent Demand Sparsity:** Low-velocity SKUs with sporadic sales exhibit higher percentage forecasting error (54.3% WAPE).
* **External Factor Unobservability:** Weather events, macroeconomic inflation, and competitor pricing were unrecorded in the dataset.
* **Lead-Time Uniformity Assumption:** Supplier lead times were modeled on standard 7-day windows; real-world supplier variability may require dynamic lead-time stochastic modeling.

---

## 16. Conclusion & Future Scope

Project FORESIGHT successfully delivered an enterprise-grade demand forecasting and inventory intelligence platform for NorthBay Living.

### Future Scope & Roadmap:
1. **FastAPI Microservice Deployment:** Expose the LightGBM model and risk engine via high-throughput RESTful endpoints for ERP/WMS integration.
2. **Automated Purchase Order EDI Integration:** Connect prescriptive PO worklists directly to vendor electronic data interchange (EDI) gateways.
3. **Hierarchical Reconciled Forecasting:** Implement MinT (Minimum Trace) reconciliation across store, city, and regional tiers.

---

## 17. Project Links & Verification Artifacts

* **GitHub Source Code Repository:** [https://github.com/MHK-123/Foresight](https://github.com/MHK-123/Foresight)
* **Interactive Dashboard Code:** [`app.py`](file:///h:/Coding/Foresight/app.py)
* **Model Artifact:** [`models/lightgbm_l2_demand_forecast.joblib`](file:///h:/Coding/Foresight/models/lightgbm_l2_demand_forecast.joblib)
* **Scored Inventory Output:** [`risk_engine_outputs/inventory_risk_scored.parquet`](file:///h:/Coding/Foresight/risk_engine_outputs/inventory_risk_scored.parquet)
* **Legal & Governance:** [`PRIVACY_POLICY.md`](file:///h:/Coding/Foresight/PRIVACY_POLICY.md) | [`TERMS_OF_SERVICE.md`](file:///h:/Coding/Foresight/TERMS_OF_SERVICE.md)
