import os
import sys
import json
import streamlit as st
import polars as pl
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------
# 1. PAGE CONFIGURATION & METADATA
# -------------------------------------------------------------
st.set_page_config(
    page_title="FORESIGHT — Retail Demand & Inventory Intelligence",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. DESIGN SYSTEM & FLAT PRINT-INSPIRED STYLING
# -------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* Global Typography */
html, body, [class*="css"], .stMarkdown, .stText, p, span, label, div {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Background & Core Workspace */
.stApp {
    background-color: #FFFFFF;
    color: #111827;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    color: #111827 !important;
    letter-spacing: -0.02em;
}

/* Flat Color-Blocked Metric Containers (No Shadows) */
.metric-card {
    background-color: #F9FAFB;
    border-radius: 8px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.metric-card.primary { border-top: 4px solid #3B82F6; }
.metric-card.danger { border-top: 4px solid #EF4444; }
.metric-card.warning { border-top: 4px solid #F59E0B; }
.metric-card.success { border-top: 4px solid #10B981; }

.metric-title {
    font-size: 0.80rem;
    font-weight: 600;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 1.80rem;
    font-weight: 800;
    color: #111827;
    line-height: 1.15;
}
.metric-subtitle {
    font-size: 0.82rem;
    color: #4B5563;
    margin-top: 5px;
    font-weight: 500;
}

/* Sidebar Flat Styling */
[data-testid="stSidebar"] {
    background-color: #F9FAFB !important;
    border-right: 1px solid #E5E7EB !important;
}

/* Buttons */
.stButton > button {
    background-color: #3B82F6 !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
    border-radius: 6px !important;
    border: none !important;
    padding: 8px 18px !important;
}
.stButton > button:hover {
    background-color: #2563EB !important;
}

/* Table Containers */
.dataframe {
    border: 1px solid #E5E7EB !important;
    font-size: 0.88rem !important;
}

/* Compact layout padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. DATA LOADING & DYNAMIC METRIC INGESTION
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORED_DATA_PATH = os.path.join(BASE_DIR, "risk_engine_outputs", "inventory_risk_scored.parquet")
TIMESERIES_PATH = os.path.join(BASE_DIR, "dashboard_data", "forecast_vs_actual_timeseries.parquet")
FEAT_IMP_PATH = os.path.join(BASE_DIR, "models", "feature_importance.csv")
METRICS_JSON_PATH = os.path.join(BASE_DIR, "dashboard_data", "model_metrics.json")

@st.cache_data(show_spinner=False)
def load_data():
    df_inv = pl.read_parquet(SCORED_DATA_PATH).to_pandas() if os.path.exists(SCORED_DATA_PATH) else pd.DataFrame()
    df_ts = pl.read_parquet(TIMESERIES_PATH).to_pandas() if os.path.exists(TIMESERIES_PATH) else pd.DataFrame()
    if not df_ts.empty and "date" in df_ts.columns:
        df_ts["date"] = pd.to_datetime(df_ts["date"])
    df_feat = pd.read_csv(FEAT_IMP_PATH) if os.path.exists(FEAT_IMP_PATH) else pd.DataFrame()
    
    meta = {}
    if os.path.exists(METRICS_JSON_PATH):
        with open(METRICS_JSON_PATH, "r") as f:
            meta = json.load(f)
    return df_inv, df_ts, df_feat, meta

df_inv, df_ts, df_feat, model_meta = load_data()

# -------------------------------------------------------------
# 4. SIDEBAR NAVIGATION & DYNAMIC FILTERS
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("### **FORESIGHT**")
    st.markdown("<span style='color: #6B7280; font-size: 0.85rem; font-weight: 500;'>Demand & Inventory Intelligence</span>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

    page = st.radio(
        "**NAVIGATION**",
        [
            "1. Executive Overview",
            "2. Stockout Risk",
            "3. Overstock / Slow Movers",
            "4. Demand Forecast",
            "5. Inventory Explorer"
        ],
        index=0
    )

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    st.markdown("#### **GLOBAL FILTERS**")
    
    # Store Filter
    all_stores = sorted(df_inv["store_id"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_stores = st.multiselect("Store ID", all_stores, default=[])
    
    # Category Filter
    all_cats = sorted(df_inv["category"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_cats = st.multiselect("Category", all_cats, default=[])
    
    # Store Format Filter
    all_formats = sorted(df_inv["store_type"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_formats = st.multiselect("Store Format", all_formats, default=[])

    # Risk Status Filter
    all_risks = sorted(df_inv["risk_status"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_risks = st.multiselect("Risk Status", all_risks, default=[])

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='font-size: 0.75rem; color: #9CA3AF; line-height: 1.4;'>
        <b>Client:</b> NorthBay Living<br>
        <b>Model:</b> {model_meta.get('model_name', 'LightGBM Model 2')}<br>
        <b>Test WAPE:</b> {model_meta.get('test_wape', 42.16)}% | <b>Bias:</b> {model_meta.get('test_bias', -0.01)}%<br>
        <b>Total Positions:</b> {len(df_inv):,} active nodes
        </div>
        """,
        unsafe_allow_html=True
    )

# Filter Dataframe Dynamically
df_filtered = df_inv.copy()
if sel_stores:
    df_filtered = df_filtered[df_filtered["store_id"].isin(sel_stores)]
if sel_cats:
    df_filtered = df_filtered[df_filtered["category"].isin(sel_cats)]
if sel_formats:
    df_filtered = df_filtered[df_filtered["store_type"].isin(sel_formats)]
if sel_risks:
    df_filtered = df_filtered[df_filtered["risk_status"].isin(sel_risks)]


# -------------------------------------------------------------
# 5. PAGE 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------
if page == "1. Executive Overview":
    st.markdown("## **Executive Overview**")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem; margin-top: -8px;'>Enterprise inventory health, working capital exposure, and network risk distribution.</p>", unsafe_allow_html=True)
    
    # Dynamic calculations directly from filtered data
    total_nodes = len(df_filtered)
    total_units = df_filtered["stock_on_hand"].sum() if not df_filtered.empty else 0
    total_cost_val = df_filtered["inventory_value_cost"].sum() if not df_filtered.empty else 0
    
    stockout_count = len(df_filtered[df_filtered["risk_status"].isin(["CRITICAL_STOCKOUT", "HIGH_STOCKOUT_RISK", "MEDIUM_STOCKOUT_RISK"])])
    stockout_pct = (stockout_count / total_nodes * 100) if total_nodes > 0 else 0
    
    overstock_count = len(df_filtered[df_filtered["risk_status"].isin(["CRITICAL_OVERSTOCK", "HIGH_OVERSTOCK", "MEDIUM_OVERSTOCK"])])
    overstock_pct = (overstock_count / total_nodes * 100) if total_nodes > 0 else 0
    overstock_capital = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_OVERSTOCK", "HIGH_OVERSTOCK", "MEDIUM_OVERSTOCK"])]["inventory_value_cost"].sum() if not df_filtered.empty else 0
    
    healthy_count = len(df_filtered[df_filtered["risk_status"] == "HEALTHY_OPTIMAL"])
    healthy_pct = (healthy_count / total_nodes * 100) if total_nodes > 0 else 0
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="metric-card primary">
                <div class="metric-title">Total Working Capital</div>
                <div class="metric-value">Rs. {total_cost_val/1e6:,.1f}M</div>
                <div class="metric-subtitle">{total_units:,.0f} units ({total_nodes:,} nodes)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="metric-card danger">
                <div class="metric-title">Stockout Risk Positions</div>
                <div class="metric-value">{stockout_count:,}</div>
                <div class="metric-subtitle">{stockout_pct:.1f}% of network positions</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="metric-card warning">
                <div class="metric-title">Overstock Trapped Capital</div>
                <div class="metric-value">Rs. {overstock_capital/1e6:,.1f}M</div>
                <div class="metric-subtitle">{overstock_count:,} positions ({overstock_pct:.1f}%)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="metric-card success">
                <div class="metric-title">Optimal / Healthy Positions</div>
                <div class="metric-value">{healthy_count:,}</div>
                <div class="metric-subtitle">{healthy_pct:.1f}% operating in 7–45d window</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Charts Row
    ch1, ch2 = st.columns([1.1, 0.9])
    
    color_map = {
        "CRITICAL_STOCKOUT": "#EF4444",
        "HIGH_STOCKOUT_RISK": "#F87171",
        "MEDIUM_STOCKOUT_RISK": "#FCA5A5",
        "CRITICAL_OVERSTOCK": "#7C3AED",
        "HIGH_OVERSTOCK": "#3B82F6",
        "MEDIUM_OVERSTOCK": "#60A5FA",
        "HEALTHY_OPTIMAL": "#10B981"
    }

    with ch1:
        st.markdown("#### **Working Capital Allocation by Risk Classification**")
        if not df_filtered.empty:
            risk_cap = (
                df_filtered.groupby("risk_status")
                .agg(Capital_Cost=("inventory_value_cost", "sum"), Node_Count=("sku_id", "count"))
                .reset_index()
                .sort_values("Capital_Cost", ascending=True)
            )
            fig_cap = px.bar(
                risk_cap,
                x="Capital_Cost",
                y="risk_status",
                orientation="h",
                text_auto=".2s",
                color="risk_status",
                color_discrete_map=color_map,
                labels={"Capital_Cost": "Capital Invested (PKR)", "risk_status": "Risk Status"}
            )
            fig_cap.update_layout(
                showlegend=False,
                margin=dict(l=10, r=20, t=10, b=20),
                height=320,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB", zeroline=False),
                yaxis=dict(showgrid=False, title="")
            )
            st.plotly_chart(fig_cap, use_container_width=True)
        else:
            st.info("No data matching current filters.")

    with ch2:
        st.markdown("#### **Network Position Share Breakdown**")
        if not df_filtered.empty:
            fig_pie = px.pie(
                df_filtered,
                names="risk_status",
                color="risk_status",
                color_discrete_map=color_map,
                hole=0.45
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=320,
                paper_bgcolor="#FFFFFF"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data matching current filters.")

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

    # Department Breakdown Table
    st.markdown("#### **Departmental Inventory Risk & Capital Profile**")
    if not df_filtered.empty:
        cat_summary = (
            df_filtered.groupby("category")
            .agg(
                Positions=("sku_id", "count"),
                Total_Stock=("stock_on_hand", "sum"),
                Cost_Basis_Capital=("inventory_value_cost", "sum"),
                Avg_Days_Supply=("days_of_supply", "mean"),
                Stockouts=("stock_on_hand", lambda s: (s == 0).sum()),
                Overstocks=("days_of_supply", lambda d: (d > 90).sum())
            )
            .reset_index()
            .sort_values("Cost_Basis_Capital", ascending=False)
        )
        cat_summary["Cost_Basis_Capital"] = cat_summary["Cost_Basis_Capital"].apply(lambda v: f"Rs. {v/1e6:,.2f}M")
        cat_summary["Avg_Days_Supply"] = cat_summary["Avg_Days_Supply"].apply(lambda d: f"{d:,.1f} days")
        st.dataframe(cat_summary, use_container_width=True, hide_index=True)


# -------------------------------------------------------------
# 6. PAGE 2: STOCKOUT RISK
# -------------------------------------------------------------
elif page == "2. Stockout Risk":
    st.markdown("## **Stockout Risk Intelligence**")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem; margin-top: -8px;'>Identify immediate inventory shortages, lead-time deficits, and required purchase orders.</p>", unsafe_allow_html=True)
    
    df_stockouts = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_STOCKOUT", "HIGH_STOCKOUT_RISK", "MEDIUM_STOCKOUT_RISK"])].copy()
    
    crit_count = len(df_stockouts[df_stockouts["risk_status"] == "CRITICAL_STOCKOUT"])
    high_count = len(df_stockouts[df_stockouts["risk_status"] == "HIGH_STOCKOUT_RISK"])
    med_count = len(df_stockouts[df_stockouts["risk_status"] == "MEDIUM_STOCKOUT_RISK"])
    lost_daily_demand = df_stockouts[df_stockouts["stock_on_hand"] == 0]["forecasted_daily_demand"].sum() if not df_stockouts.empty else 0
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            f"""
            <div class="metric-card danger">
                <div class="metric-title">Critical Stockouts (Stock=0)</div>
                <div class="metric-value">{crit_count:,}</div>
                <div class="metric-subtitle">Zero physical inventory</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with s2:
        st.markdown(
            f"""
            <div class="metric-card warning">
                <div class="metric-title">High Stockout Risk</div>
                <div class="metric-value">{high_count:,}</div>
                <div class="metric-subtitle">Stock &lt; Safety Stock buffer</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with s3:
        st.markdown(
            f"""
            <div class="metric-card primary">
                <div class="metric-title">Medium Stockout Risk</div>
                <div class="metric-value">{med_count:,}</div>
                <div class="metric-subtitle">Breach within 7-day lead time</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with s4:
        st.markdown(
            f"""
            <div class="metric-card danger">
                <div class="metric-title">Active Daily Lost Demand</div>
                <div class="metric-value">{lost_daily_demand:,.0f}</div>
                <div class="metric-subtitle">Units/day unfulfilled</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Visual Breakdown by Store & Category
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("#### **Top Stores Facing Critical Stockouts**")
        if not df_stockouts.empty and crit_count > 0:
            st_so = (
                df_stockouts[df_stockouts["risk_status"] == "CRITICAL_STOCKOUT"]
                .groupby(["store_id", "city", "store_type"])
                .agg(Stockout_SKUs=("sku_id", "count"))
                .reset_index()
                .sort_values("Stockout_SKUs", ascending=False)
                .head(10)
            )
            fig_st_so = px.bar(
                st_so,
                x="Stockout_SKUs",
                y="store_id",
                orientation="h",
                color="store_type",
                color_discrete_sequence=["#EF4444", "#F59E0B", "#3B82F6", "#10B981"],
                labels={"Stockout_SKUs": "Zero-Stock Positions", "store_id": "Store ID"}
            )
            fig_st_so.update_layout(
                margin=dict(l=10, r=20, t=10, b=20),
                height=280,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_st_so, use_container_width=True)
        else:
            st.info("No critical stockouts found for active filters.")
        
    with sc2:
        st.markdown("#### **Stockout Risk Distribution by Category**")
        if not df_stockouts.empty:
            cat_so = (
                df_stockouts
                .groupby(["category", "risk_status"])
                .size()
                .reset_index(name="Positions")
            )
            fig_cat_so = px.bar(
                cat_so,
                x="category",
                y="Positions",
                color="risk_status",
                color_discrete_map={
                    "CRITICAL_STOCKOUT": "#EF4444",
                    "HIGH_STOCKOUT_RISK": "#F59E0B",
                    "MEDIUM_STOCKOUT_RISK": "#FCA5A5"
                },
                barmode="stack"
            )
            fig_cat_so.update_layout(
                margin=dict(l=10, r=10, t=10, b=40),
                height=280,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(tickangle=-30, showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                legend=dict(orientation="h", y=1.15, x=0)
            )
            st.plotly_chart(fig_cat_so, use_container_width=True)
        else:
            st.info("No stockouts matching current filters.")

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Priority Replenishment Queue
    st.markdown("#### **Prescriptive Replenishment Worklist (Sorted by Sales Velocity)**")
    if not df_stockouts.empty:
        df_stockouts["suggested_po_qty"] = np.ceil(
            (df_stockouts["safety_stock"] + df_stockouts["forecast_14d_demand"]) - df_stockouts["stock_on_hand"]
        ).astype(int)
        
        stockout_cols = [
            "store_id", "sku_id", "sku_name", "category", "store_type",
            "stock_on_hand", "safety_stock", "forecasted_daily_demand",
            "days_of_supply", "suggested_po_qty", "risk_status", "recommended_action"
        ]
        df_so_display = df_stockouts[stockout_cols].sort_values("forecasted_daily_demand", ascending=False)
        
        st.dataframe(
            df_so_display.head(100),
            use_container_width=True,
            hide_index=True,
            column_config={
                "forecasted_daily_demand": st.column_config.NumberColumn("Daily Velocity", format="%.2f units"),
                "days_of_supply": st.column_config.NumberColumn("Days Supply", format="%.1f d"),
                "suggested_po_qty": st.column_config.NumberColumn("Suggested PO (Units)", format="%d")
            }
        )
    else:
        st.info("No replenishment actions needed for current filters.")


# -------------------------------------------------------------
# 7. PAGE 3: OVERSTOCK / SLOW MOVERS
# -------------------------------------------------------------
elif page == "3. Overstock / Slow Movers":
    st.markdown("## **Overstock & Slow-Mover Capital Optimization**")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem; margin-top: -8px;'>Identify trapped working capital, stagnant inventory, and candidates for clearance markdowns.</p>", unsafe_allow_html=True)
    
    df_overstock = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_OVERSTOCK", "HIGH_OVERSTOCK", "MEDIUM_OVERSTOCK"])].copy()
    
    crit_ov = len(df_overstock[df_overstock["risk_status"] == "CRITICAL_OVERSTOCK"])
    high_ov = len(df_overstock[df_overstock["risk_status"] == "HIGH_OVERSTOCK"])
    med_ov = len(df_overstock[df_overstock["risk_status"] == "MEDIUM_OVERSTOCK"])
    trapped_capital = df_overstock["inventory_value_cost"].sum() if not df_overstock.empty else 0
    
    o1, o2, o3, o4 = st.columns(4)
    with o1:
        st.markdown(
            f"""
            <div class="metric-card danger">
                <div class="metric-title">Critical Overstock / Dead Stock</div>
                <div class="metric-value">{crit_ov:,}</div>
                <div class="metric-subtitle">DOS &gt; 120d + Stale Restock</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with o2:
        st.markdown(
            f"""
            <div class="metric-card warning">
                <div class="metric-title">High Overstock</div>
                <div class="metric-value">{high_ov:,}</div>
                <div class="metric-subtitle">DOS &gt; 90 days of supply</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with o3:
        st.markdown(
            f"""
            <div class="metric-card primary">
                <div class="metric-title">Medium Overstock</div>
                <div class="metric-value">{med_ov:,}</div>
                <div class="metric-subtitle">45d &lt; DOS &le; 90d</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with o4:
        st.markdown(
            f"""
            <div class="metric-card warning">
                <div class="metric-title">Total Trapped Capital</div>
                <div class="metric-value">Rs. {trapped_capital/1e6:,.1f}M</div>
                <div class="metric-subtitle">Cost basis in excess inventory</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Charts Row
    oc1, oc2 = st.columns(2)
    with oc1:
        st.markdown("#### **Trapped Working Capital by Category**")
        if not df_overstock.empty:
            cat_ov = (
                df_overstock.groupby("category")
                .agg(Trapped_Capital=("inventory_value_cost", "sum"))
                .reset_index()
                .sort_values("Trapped_Capital", ascending=True)
            )
            fig_cat_ov = px.bar(
                cat_ov,
                x="Trapped_Capital",
                y="category",
                orientation="h",
                color="Trapped_Capital",
                color_continuous_scale="Blues",
                labels={"Trapped_Capital": "Trapped Capital (PKR)", "category": "Category"}
            )
            fig_cat_ov.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                margin=dict(l=10, r=20, t=10, b=20),
                height=300,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB")
            )
            st.plotly_chart(fig_cat_ov, use_container_width=True)
        else:
            st.info("No overstock matching current filters.")
        
    with oc2:
        st.markdown("#### **Staleness Profile (Days of Supply vs. Restock Recency)**")
        if not df_overstock.empty:
            sample_ov = df_overstock.head(1000)
            fig_scatter = px.scatter(
                sample_ov,
                x="days_since_last_restock",
                y="days_of_supply",
                color="risk_status",
                size="inventory_value_cost",
                hover_data=["sku_name", "store_id", "category"],
                color_discrete_map={
                    "CRITICAL_OVERSTOCK": "#7C3AED",
                    "HIGH_OVERSTOCK": "#3B82F6",
                    "MEDIUM_OVERSTOCK": "#60A5FA"
                },
                labels={"days_since_last_restock": "Days Since Last Restock", "days_of_supply": "Days of Supply (DOS)"}
            )
            fig_scatter.update_layout(
                margin=dict(l=10, r=10, t=10, b=20),
                height=300,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                yaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                legend=dict(orientation="h", y=1.15, x=0)
            )
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No overstock positions found.")

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Clearance Candidates Table
    st.markdown("#### **Dead Stock & Clearance Markdown Candidates**")
    if not df_overstock.empty:
        overstock_cols = [
            "store_id", "sku_id", "sku_name", "category", "stock_on_hand",
            "days_since_last_restock", "forecasted_daily_demand", "days_of_supply",
            "inventory_value_cost", "risk_status", "recommended_action"
        ]
        df_ov_display = df_overstock[overstock_cols].sort_values("inventory_value_cost", ascending=False)
        
        st.dataframe(
            df_ov_display.head(100),
            use_container_width=True,
            hide_index=True,
            column_config={
                "inventory_value_cost": st.column_config.NumberColumn("Trapped Capital (PKR)", format="Rs. %,.0f"),
                "days_of_supply": st.column_config.NumberColumn("Days Supply", format="%.0f d"),
                "days_since_last_restock": st.column_config.NumberColumn("Restock Recency", format="%d days ago"),
                "forecasted_daily_demand": st.column_config.NumberColumn("Daily Velocity", format="%.2f")
            }
        )


# -------------------------------------------------------------
# 8. PAGE 4: DEMAND FORECAST
# -------------------------------------------------------------
elif page == "4. Demand Forecast":
    st.markdown("## **Machine Learning Demand Forecasting Engine**")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem; margin-top: -8px;'>Multi-horizon predictive modeling powered by LightGBM Regressor (Model 2).</p>", unsafe_allow_html=True)
    
    # Dynamic Model Performance Metric Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f"""
            <div class="metric-card primary">
                <div class="metric-title">Model Architecture</div>
                <div class="metric-value" style="font-size: 1.45rem;">LightGBM GBDT</div>
                <div class="metric-subtitle">Optimized L2 Loss ({model_meta.get('n_trees', 70)} trees)</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f"""
            <div class="metric-card success">
                <div class="metric-title">Test WAPE Accuracy</div>
                <div class="metric-value">{model_meta.get('test_wape', 42.16)}%</div>
                <div class="metric-subtitle">&plus;{model_meta.get('wape_gain_pct', 11.3)}% gain over Baseline</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card success">
                <div class="metric-title">Test RMSE</div>
                <div class="metric-value">{model_meta.get('test_rmse', 1.183)}</div>
                <div class="metric-subtitle">&plus;{model_meta.get('rmse_gain_pct', 20.3)}% variance reduction</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f"""
            <div class="metric-card primary">
                <div class="metric-title">Network Forecast Bias</div>
                <div class="metric-value">{model_meta.get('test_bias', -0.01)}%</div>
                <div class="metric-subtitle">Zero systematic bias</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Interactive Time Series Forecast Explorer
    st.markdown("#### **Interactive Time-Series Forecast Explorer (Test Period: H2 2025)**")
    
    if not df_ts.empty:
        fc1, fc2 = st.columns([1, 2])
        with fc1:
            avail_stores = sorted(df_ts["store_id"].unique().tolist())
            sel_ts_store = st.selectbox("Select Store", avail_stores, index=0)
            
            avail_skus = sorted(df_ts[df_ts["store_id"] == sel_ts_store]["sku_id"].unique().tolist())
            sel_ts_sku = st.selectbox("Select SKU", avail_skus, index=0)
            
            sku_name_match = df_inv[df_inv["sku_id"] == sel_ts_sku]["sku_name"].values if not df_inv.empty else []
            sku_name_str = sku_name_match[0] if len(sku_name_match) > 0 else sel_ts_sku
            st.markdown(f"**Item:** `{sel_ts_sku}` — *{sku_name_str}*")
            
            show_baselines = st.checkbox("Show Heuristic Baselines (SMA 28 & Lag 7)", value=True)

        with fc2:
            node_ts = df_ts[(df_ts["store_id"] == sel_ts_store) & (df_ts["sku_id"] == sel_ts_sku)].sort_values("date")
            
            fig_ts = go.Figure()
            # Actual
            fig_ts.add_trace(go.Scatter(
                x=node_ts["date"],
                y=node_ts["daily_quantity"],
                mode="lines+markers",
                name="Actual Daily Sales",
                line=dict(color="#111827", width=2),
                marker=dict(size=4)
            ))
            # Forecast
            fig_ts.add_trace(go.Scatter(
                x=node_ts["date"],
                y=node_ts["forecasted_demand"],
                mode="lines",
                name="LightGBM ML Forecast",
                line=dict(color="#3B82F6", width=2.5)
            ))
            
            if show_baselines:
                fig_ts.add_trace(go.Scatter(
                    x=node_ts["date"],
                    y=node_ts["baseline_sma28"],
                    mode="lines",
                    name="28d Rolling SMA Baseline",
                    line=dict(color="#10B981", width=1.5, dash="dash")
                ))
                fig_ts.add_trace(go.Scatter(
                    x=node_ts["date"],
                    y=node_ts["baseline_lag7"],
                    mode="lines",
                    name="Lag-7 Baseline",
                    line=dict(color="#F59E0B", width=1, dash="dot")
                ))
                
            fig_ts.update_layout(
                margin=dict(l=10, r=10, t=10, b=20),
                height=340,
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#F9FAFB",
                xaxis=dict(showgrid=True, gridcolor="#E5E7EB"),
                yaxis=dict(showgrid=True, gridcolor="#E5E7EB", title="Daily Quantity (Units)"),
                legend=dict(orientation="h", y=1.12, x=0)
            )
            st.plotly_chart(fig_ts, use_container_width=True)
    else:
        st.info("Time-series test dataset not loaded.")

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    # Feature Importance Row
    if not df_feat.empty:
        st.markdown("#### **Top 15 Machine Learning Demand Drivers (Gain Importance)**")
        fig_feat = px.bar(
            df_feat.head(15).sort_values("Importance", ascending=True),
            x="Importance",
            y="Feature",
            orientation="h",
            color="Importance",
            color_continuous_scale="Blues"
        )
        fig_feat.update_layout(
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=10, r=20, t=10, b=20),
            height=320,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#F9FAFB",
            xaxis=dict(showgrid=True, gridcolor="#E5E7EB")
        )
        st.plotly_chart(fig_feat, use_container_width=True)


# -------------------------------------------------------------
# 9. PAGE 5: INVENTORY EXPLORER
# -------------------------------------------------------------
elif page == "5. Inventory Explorer":
    st.markdown("## **Inventory Explorer & Operational Action Center**")
    st.markdown("<p style='color: #4B5563; font-size: 0.95rem; margin-top: -8px;'>Search, inspect, and export SKU-level inventory positions and prescriptive actions.</p>", unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search by SKU Name, SKU ID, or Brand", placeholder="Type SKU name or ID (e.g., Bread, Milk, SKU00002)...")
    
    df_exp = df_filtered.copy()
    if search_query:
        mask = (
            df_exp["sku_name"].str.contains(search_query, case=False, na=False) |
            df_exp["sku_id"].str.contains(search_query, case=False, na=False) |
            df_exp["brand"].str.contains(search_query, case=False, na=False)
        )
        df_exp = df_exp[mask]

    st.markdown(f"Showing **{len(df_exp):,}** inventory positions matching active filters.")
    
    exp_cols = [
        "store_id", "city", "sku_id", "sku_name", "category", "brand",
        "stock_on_hand", "safety_stock", "forecasted_daily_demand", "days_of_supply",
        "days_since_last_restock", "inventory_value_cost", "risk_status",
        "risk_reason", "recommended_action"
    ]
    
    csv_data = df_exp[exp_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Worklist to CSV",
        data=csv_data,
        file_name="foresight_inventory_action_worklist.csv",
        mime="text/csv"
    )
    
    st.dataframe(
        df_exp[exp_cols].head(250),
        use_container_width=True,
        hide_index=True,
        column_config={
            "forecasted_daily_demand": st.column_config.NumberColumn("Daily Velocity", format="%.2f"),
            "days_of_supply": st.column_config.NumberColumn("Days Supply", format="%.1f d"),
            "days_since_last_restock": st.column_config.NumberColumn("Restock Recency", format="%d d"),
            "inventory_value_cost": st.column_config.NumberColumn("Trapped Capital", format="Rs. %,.0f")
        }
    )

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)
    
    with st.expander("🔬 **Synthetic Ground-Truth Validation & Model Explainability Notes**"):
        st.markdown(
            """
            * **Synthetic Anomaly Recall:** The underlying risk scoring engine achieved **100.0% Detection Recall** on both injected stockouts ($2,703 / 2,703$ nodes) and intentional slow movers ($8,946 / 8,946$ nodes).
            * **Zero Data Leakage:** Ground-truth flags from `sku_inventory_flags` were strictly excluded from model training and scoring, serving purely as post-hoc validation benchmarks.
            * **Organic Detections:** The engine flags both synthetically injected defects and organic retail inventory imbalances (e.g. natural store stockouts and dead stock).
            """
        )
