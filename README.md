# Project FORESIGHT Retail Demand & Inventory Intelligence

Client: NorthBay Living  
Role: Data Science & Analytics Intern (Zidio Internship Project)  
Tech Stack: Python, Polars, Pandas, LightGBM, Plotly, Streamlit  

---

## Project Overview

Project FORESIGHT is an end-to-end retail demand forecasting and inventory intelligence system built for NorthBay Living. NorthBay Living operates 30 retail stores across 12 cities with a catalog of 5,000 products.

The goal of this project is to solve two core retail problems:
1. Prevent stockouts on bestselling items so sales are not lost.
2. Identify overstock and slow-moving items so working capital is not trapped.

---

## Project Workflow and Key Results

1. Business & Dataset Understanding:
   - Inspected 9.94 million transactions from 2022 to 2025 across 30 stores and 5,000 products.

2. Data Cleaning:
   - Fixed data types, standardized dates, and kept intentional anomaly flags for testing.

3. Exploratory Data Analysis (EDA):
   - Found steady ~6% annual growth, clear November-December holiday peaks, and strong Pareto concentration (top 20% products drive 58.8% of volume).

4. Feature Engineering:
   - Created 52 features including calendar cycles, demand lags, rolling averages, product prices, and store foot traffic.

5. Baseline Forecasting:
   - Tested 5 simple baseline models. The best baseline achieved 47.54% WAPE.

6. Machine Learning Forecasting:
   - Trained a LightGBM model that achieved 42.16% WAPE, 1.183 RMSE, and -0.01% bias, outperforming all baselines.

7. Model Evaluation & Diagnosis:
   - High-velocity bestselling items reached 20.75% WAPE with zero systematic bias across categories and store formats.

8. Inventory Risk Scoring Engine:
   - Scored 26,408 store-product positions. Identified 5,209 stockout positions and 17,991 overstock positions with 100% recall on test anomalies.

9. Streamlit Dashboard:
   - Built a 5-page interactive dashboard with dynamic metrics, interactive charts, and exportable action lists.

---

## Streamlit Dashboard Pages

1. Executive Overview: Shows total inventory value, risk distribution, and department health.
2. Stockout Risk: Shows critical zero-stock items and suggested purchase order quantities.
3. Overstock / Slow Movers: Shows trapped capital, stale inventory, and clearance markdown candidates.
4. Demand Forecast: Shows actual versus forecasted demand, baselines, and top model features.
5. Inventory Explorer: Allows searching, filtering, and downloading complete inventory action worklists.

---

## How to Run the Dashboard Locally

1. Install required packages:
```bash
pip install streamlit polars pandas numpy lightgbm plotly joblib
```

2. Start the Streamlit app:
```bash
streamlit run app.py
```

3. Open your browser at:
`http://localhost:8501`

---

## Repository Structure

```text
├── app.py                                # Main Streamlit dashboard application
├── dashboard_data/                       # Pre-computed time series and model metrics
│   ├── forecast_vs_actual_timeseries.parquet
│   └── model_metrics.json
├── models/                               # Trained LightGBM model files
│   ├── lightgbm_l1_demand_forecast.joblib
│   ├── lightgbm_l2_demand_forecast.joblib
│   └── feature_importance.csv
├── risk_engine_outputs/                  # Risk scored inventory dataset
│   ├── inventory_risk_scored.parquet
│   └── inventory_risk_scored_sample.csv
├── eda_charts/                           # Visualizations from Step 3 EDA
├── features/                             # Sample engineered feature dataset
│   └── daily_store_sku_features_sample.csv
├── requirements.txt                      # Application dependencies
├── PRIVACY_POLICY.md                     # Data governance and privacy disclosure
├── TERMS_OF_SERVICE.md                   # Enterprise terms and forecasting disclaimer
└── README.md                             # Project documentation
```

---

## Governance & Compliance

* **Privacy Policy:** [PRIVACY_POLICY.md](file:///h:/Coding/Foresight/PRIVACY_POLICY.md)
* **Terms of Service:** [TERMS_OF_SERVICE.md](file:///h:/Coding/Foresight/TERMS_OF_SERVICE.md)

