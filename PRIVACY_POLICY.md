# Privacy Policy

**Last Updated: August 28, 2026**

Project FORESIGHT ("FORESIGHT", "we", "us", or "our") provides enterprise demand forecasting and inventory risk intelligence for retail organizations, including NorthBay Living. This Privacy Policy describes how data is handled, processed, and protected within the FORESIGHT platform.

---

## 1. Information We Process

FORESIGHT processes enterprise retail and operational datasets exclusively for analytical, predictive modeling, and inventory optimization purposes:
* **Transaction Records:** Historical store-level and channel-level product sales quantities, prices, discounts, and transaction dates.
* **Inventory Data:** Physical stock on hand, safety stock thresholds, reorder points, and supplier lead times.
* **Product & Store Metadata:** SKU IDs, category hierarchies, store locations, and retail formats.

**Non-PII Guarantee:** FORESIGHT does not collect, store, or process Personally Identifiable Information (PII) such as customer names, payment card details, phone numbers, or residential addresses.

---

## 2. Purpose of Data Processing

All datasets ingested into FORESIGHT are strictly used to:
* Generate store-SKU level demand forecasts using LightGBM machine learning models.
* Classify operational inventory risks (stockout deficits, overstock positions, dead stock).
* Calculate prescriptive replenishment quantities, reorder schedules, and inventory transfer recommendations.
* Render interactive diagnostic dashboards and performance metrics for supply chain decision-makers.

---

## 3. Data Storage & Security

* **Local & Isolated Execution:** In local development environments, all raw transaction logs, feature stores, and model binaries reside within secured local directories.
* **Access Controls:** Production deployments implement role-based access control (RBAC) to ensure only authorized retail inventory analysts and executives can view enterprise metrics.
* **No Third-Party Sharing:** FORESIGHT does not sell, rent, or distribute retail operational data to third-party advertisers or external data brokers.

---

## 4. Machine Learning & Model Transparency

* **No Automated Unsupervised Actions:** Predictions and recommendations produced by FORESIGHT are decision-support aids. They do not execute automated financial transactions or supplier purchase orders without human review.
* **Explainability:** All risk scores are rule-governed and explainable based on deterministic inventory thresholds and validated machine-learning demand projections.

---

## 5. Contact & Governance

For inquiries regarding data governance, audit trails, or privacy compliance within FORESIGHT, please contact the NorthBay Living Data Analytics & Supply Chain Governance Team.
