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
# 1. PAGE CONFIGURATION
# -------------------------------------------------------------
st.set_page_config(
    page_title="FORESIGHT — Retail Demand & Inventory Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# 2. DESIGN SYSTEM & HIGH-CONTRAST CSS
# -------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg-main: #FFFFFF;
    --text-primary: #0F172A;
    --text-secondary: #334155;
    --text-muted: #64748B;
    --border-color: #CBD5E1;
    --card-bg: #F8FAFC;
    --primary-blue: #2563EB;
    --emerald-green: #059669;
    --amber-warning: #D97706;
    --rose-danger: #E11D48;
    --purple-overstock: #7C3AED;
}

/* Typography without breaking Streamlit Icon Ligatures */
html, body, .stMarkdown p, .stText, label, .metric-title, .metric-value, .metric-subtitle {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}

/* PRESERVE STREAMLIT MATERIAL ICONS & SYMBOLS (Prevents 'keyboard_double_arrow' text) */
.material-symbols-rounded,
.material-symbols-outlined,
.material-icons,
[data-testid="stIconMaterial"],
[data-testid="stSidebarCollapseButton"] span,
[data-testid="stSidebarCollapseButton"] i,
[data-testid="collapsedControl"] span {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    color: #0F172A !important;
    letter-spacing: -0.025em;
    margin-bottom: 0.5rem;
}

/* Dropdowns & Popovers */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
div[data-baseweb="popover"] > div {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.1) !important;
}

li[role="option"],
ul[role="listbox"] li {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
    font-size: 0.90rem !important;
    font-weight: 500 !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #F1F5F9 !important;
}

li[role="option"]:hover,
ul[role="listbox"] li:hover {
    background-color: #EFF6FF !important;
    color: #1D4ED8 !important;
}

li[role="option"]:hover * {
    color: #1D4ED8 !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 6px !important;
}

div[data-baseweb="select"] [data-baseweb="tag"] {
    background-color: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
    color: #1D4ED8 !important;
    font-weight: 600 !important;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #F8FAFC !important;
    border-right: 1px solid #E2E8F0 !important;
    padding: 1.2rem 1rem !important;
}

[data-testid="stSidebar"] label {
    font-weight: 700 !important;
    color: #1E293B !important;
    font-size: 0.80rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}

/* Sidebar Profile Block */
.user-profile-card {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 10px 12px;
    margin: 12px 0 16px 0;
}
.user-avatar-icon {
    width: 34px;
    height: 34px;
    border-radius: 6px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2563EB;
}

/* Radio Navigation */
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 6px;
    font-weight: 600 !important;
    color: #1E293B !important;
    transition: all 0.12s ease-in-out;
    cursor: pointer;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background-color: #F1F5F9;
    border-color: #CBD5E1;
    transform: translateX(2px);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label[data-checked="true"] {
    background-color: #EFF6FF !important;
    border-color: #3B82F6 !important;
    color: #1D4ED8 !important;
}

/* Metric Cards */
.metric-card {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 20px;
    min-height: 140px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: transform 0.15s ease, border-color 0.15s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: #94A3B8;
}

.metric-card.primary { border-top: 5px solid #2563EB; }
.metric-card.danger { border-top: 5px solid #E11D48; }
.metric-card.warning { border-top: 5px solid #D97706; }
.metric-card.success { border-top: 5px solid #059669; }

.metric-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #475569;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 2.1rem;
    font-weight: 900;
    color: #0F172A;
    line-height: 1.1;
    letter-spacing: -0.03em;
}
.metric-subtitle {
    font-size: 0.88rem;
    color: #334155;
    font-weight: 500;
    margin-top: 8px;
}

/* Buttons */
.stButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 8px 18px !important;
}
.stButton > button:hover {
    background-color: #1D4ED8 !important;
}

/* Chat */
.chat-user {
    background-color: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px 10px 2px 10px;
    padding: 12px 16px;
    color: #1E3A8A;
    font-weight: 600;
    margin: 8px 0;
    width: fit-content;
    max-width: 80%;
    margin-left: auto;
}
.chat-assistant {
    background-color: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #2563EB;
    border-radius: 4px 10px 10px 4px;
    padding: 14px 18px;
    color: #0F172A;
    margin: 8px 0 16px 0;
    width: 100%;
}

.alert-box {
    background-color: #F8FAFC;
    border-left: 4px solid #2563EB;
    padding: 12px 16px;
    border-radius: 0 6px 6px 0;
    margin: 12px 0;
    font-size: 0.9rem;
    color: #1E293B;
}

.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 2.5rem !important;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. GLOBAL PLOTLY STYLING THEME
# -------------------------------------------------------------
def apply_chart_theme(fig, height=330):
    fig.update_layout(
        font=dict(family="Outfit, sans-serif", size=12, color="#0F172A"),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#F8FAFC",
        margin=dict(l=20, r=20, t=30, b=20),
        height=height,
        hoverlabel=dict(bgcolor="#0F172A", font_size=12, font_family="Outfit", font_color="#FFFFFF"),
        xaxis=dict(showgrid=True, gridcolor="#E2E8F0", linecolor="#CBD5E1", tickfont=dict(size=11, color="#334155", family="Outfit"), title_font=dict(size=12, color="#0F172A", family="Outfit")),
        yaxis=dict(showgrid=True, gridcolor="#E2E8F0", linecolor="#CBD5E1", tickfont=dict(size=11, color="#334155", family="Outfit"), title_font=dict(size=12, color="#0F172A", family="Outfit")),
        legend=dict(font=dict(size=11, color="#0F172A", family="Outfit"), bgcolor="rgba(255,255,255,0.85)", bordercolor="#E2E8F0", borderwidth=1)
    )
    return fig

# -------------------------------------------------------------
# 4. DATA LOADING & INGESTION
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCORED_DATA_PATH = os.path.join(BASE_DIR, "risk_engine_outputs", "inventory_risk_scored.parquet")
TIMESERIES_PATH = os.path.join(BASE_DIR, "dashboard_data", "forecast_vs_actual_timeseries.parquet")
FEAT_IMP_PATH = os.path.join(BASE_DIR, "models", "feature_importance.csv")
METRICS_JSON_PATH = os.path.join(BASE_DIR, "dashboard_data", "model_metrics.json")

@st.cache_data(show_spinner=False)
def load_all_data():
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

df_inv, df_ts, df_feat, model_meta = load_all_data()

# -------------------------------------------------------------
# 5. SIDEBAR WITH CLEAN PROFILE & BRANDING (NO BROKEN LIGATURES)
# -------------------------------------------------------------
with st.sidebar:
    # Top Branding Block
    st.markdown(
        """
        <div style='margin-bottom: 8px;'>
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <span style='font-size: 1.45rem; font-weight: 900; color: #0F172A; letter-spacing: -0.03em;'>FORESIGHT</span>
                <span style='font-size: 0.72rem; font-weight: 700; background: #DBEAFE; color: #1D4ED8; padding: 2px 8px; border-radius: 4px;'>v1.0</span>
            </div>
            <div style='font-size: 0.82rem; font-weight: 600; color: #475569; margin-top: 2px;'>Demand & Inventory Intelligence</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Professional Outline User / Organization Profile Card (Clean SVG Avatar)
    st.markdown(
        """
        <div class="user-profile-card">
            <div class="user-avatar-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div style='line-height: 1.25;'>
                <div style='font-size: 0.85rem; font-weight: 700; color: #0F172A;'>NorthBay Living</div>
                <div style='font-size: 0.75rem; color: #64748B;'>Retail Analytics Workspace</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr style='margin: 8px 0 14px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

    page = st.radio(
        "OPERATIONAL VIEWS",
        [
            "1. Executive Overview",
            "2. Stockout Risk",
            "3. Overstock / Slow Movers",
            "4. Demand Forecast",
            "5. Inventory Explorer",
            "6. Priority Action Center",
            "7. What-If Simulator",
            "8. Intelligence Assistant"
        ],
        index=0
    )

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.80rem; font-weight: 800; color: #0F172A; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>FILTER NETWORK</div>", unsafe_allow_html=True)
    
    all_stores = sorted(df_inv["store_id"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_stores = st.multiselect("Store Location", all_stores, placeholder="All 30 Stores", default=[])
    
    all_cats = sorted(df_inv["category"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_cats = st.multiselect("Merchandise Category", all_cats, placeholder="All 12 Categories", default=[])
    
    all_formats = sorted(df_inv["store_type"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_formats = st.multiselect("Store Format", all_formats, placeholder="All Formats", default=[])

    all_risks = sorted(df_inv["risk_status"].dropna().unique().tolist()) if not df_inv.empty else []
    sel_risks = st.multiselect("Risk Classification", all_risks, placeholder="All Risk Tiers", default=[])

    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px; font-size: 0.78rem; color: #334155; line-height: 1.5;'>
        <b style='color: #0F172A;'>Engine Parameters</b><br>
        • <b>Forecasting Model:</b> {model_meta.get('model_name', 'LightGBM Model 2')}<br>
        • <b>Out-of-Sample WAPE:</b> <span style='color: #059669; font-weight: 700;'>{model_meta.get('test_wape', 42.16)}%</span><br>
        • <b>Inventory Nodes:</b> {len(df_inv):,} positions
        </div>
        """,
        unsafe_allow_html=True
    )

df_filtered = df_inv.copy()
if sel_stores:
    df_filtered = df_filtered[df_filtered["store_id"].isin(sel_stores)]
if sel_cats:
    df_filtered = df_filtered[df_filtered["category"].isin(sel_cats)]
if sel_formats:
    df_filtered = df_filtered[df_filtered["store_type"].isin(sel_formats)]
if sel_risks:
    df_filtered = df_filtered[df_filtered["risk_status"].isin(sel_risks)]

COLOR_MAP = {
    "CRITICAL_STOCKOUT": "#E11D48",
    "HIGH_STOCKOUT_RISK": "#F43F5E",
    "MEDIUM_STOCKOUT_RISK": "#FDA4AF",
    "CRITICAL_OVERSTOCK": "#7C3AED",
    "HIGH_OVERSTOCK": "#2563EB",
    "MEDIUM_OVERSTOCK": "#60A5FA",
    "HEALTHY_OPTIMAL": "#059669"
}

# -------------------------------------------------------------
# 6. PAGE 1: EXECUTIVE OVERVIEW
# -------------------------------------------------------------
if page == "1. Executive Overview":
    st.markdown("## **Executive Overview**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Enterprise inventory health, working capital exposure, and risk distribution across NorthBay Living.</p>", unsafe_allow_html=True)
    
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
        st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Total Working Capital</div><div class="metric-value">Rs. {total_cost_val/1e6:,.1f}M</div></div><div class="metric-subtitle"><b>{total_units:,.0f}</b> units across <b>{total_nodes:,}</b> nodes</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card danger"><div><div class="metric-badge" style="color: #BE123C;">Stockout Deficit Positions</div><div class="metric-value" style="color: #BE123C;">{stockout_count:,}</div></div><div class="metric-subtitle"><b style="color: #BE123C;">{stockout_pct:.1f}%</b> of positions face lost revenue</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card warning"><div><div class="metric-badge" style="color: #B45309;">Overstock Trapped Capital</div><div class="metric-value" style="color: #B45309;">Rs. {overstock_capital/1e6:,.1f}M</div></div><div class="metric-subtitle"><b style="color: #B45309;">{overstock_count:,}</b> positions ({overstock_pct:.1f}% of network)</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card success"><div><div class="metric-badge" style="color: #047857;">Healthy / Optimal Stock</div><div class="metric-value" style="color: #047857;">{healthy_count:,}</div></div><div class="metric-subtitle"><b style="color: #047857;">{healthy_pct:.1f}%</b> operating in 7–45d target window</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    ch1, ch2 = st.columns([1.15, 0.85])
    with ch1:
        st.markdown("#### **Working Capital Invested by Risk Classification**")
        if not df_filtered.empty:
            risk_cap = df_filtered.groupby("risk_status").agg(Capital_Cost=("inventory_value_cost", "sum")).reset_index().sort_values("Capital_Cost", ascending=True)
            fig_cap = px.bar(risk_cap, x="Capital_Cost", y="risk_status", orientation="h", color="risk_status", color_discrete_map=COLOR_MAP, text=risk_cap["Capital_Cost"].apply(lambda v: f"Rs. {v/1e6:,.1f}M"), labels={"Capital_Cost": "Cost Basis Capital (PKR)", "risk_status": ""})
            fig_cap.update_traces(textposition="outside", textfont=dict(color="#0F172A", size=11, family="Outfit"), hovertemplate="<b>%{y}</b><br>Capital: Rs. %{x:,.0f}<extra></extra>")
            fig_cap = apply_chart_theme(fig_cap, height=330)
            fig_cap.update_layout(showlegend=False, xaxis=dict(showgrid=True, zeroline=False))
            st.plotly_chart(fig_cap, width="stretch")
        else:
            st.info("No data available.")

    with ch2:
        st.markdown("#### **Network Position Distribution**")
        if not df_filtered.empty:
            fig_pie = px.pie(df_filtered, names="risk_status", color="risk_status", color_discrete_map=COLOR_MAP, hole=0.52)
            fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont=dict(family="Outfit", size=11, color="#FFFFFF"), hovertemplate="<b>%{label}</b><br>Count: %{value:,} (%{percent})<extra></extra>", marker=dict(line=dict(color="#FFFFFF", width=2)))
            fig_pie = apply_chart_theme(fig_pie, height=330)
            fig_pie.update_layout(showlegend=False, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_pie, width="stretch")
        else:
            st.info("No data available.")

    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("#### **Merchandise Department Health & Capital Exposure**")
    if not df_filtered.empty:
        cat_summary = df_filtered.groupby("category").agg(Positions=("sku_id", "count"), Physical_Stock=("stock_on_hand", "sum"), Working_Capital=("inventory_value_cost", "sum"), Avg_Days_Supply=("days_of_supply", "mean"), Stockouts=("stock_on_hand", lambda s: (s == 0).sum()), Overstocks=("days_of_supply", lambda d: (d > 90).sum())).reset_index().sort_values("Working_Capital", ascending=False)
        cat_summary["Working_Capital"] = cat_summary["Working_Capital"].apply(lambda v: f"Rs. {v/1e6:,.2f}M")
        cat_summary["Avg_Days_Supply"] = cat_summary["Avg_Days_Supply"].apply(lambda d: f"{d:,.1f} days")
        cat_summary["Physical_Stock"] = cat_summary["Physical_Stock"].apply(lambda u: f"{u:,.0f} units")
        st.dataframe(cat_summary, width="stretch", hide_index=True)

# -------------------------------------------------------------
# 7. PAGE 2: STOCKOUT RISK
# -------------------------------------------------------------
elif page == "2. Stockout Risk":
    st.markdown("## **Stockout Risk Intelligence**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Identify immediate inventory shortages, lead-time deficits, and required purchase orders.</p>", unsafe_allow_html=True)
    
    df_stockouts = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_STOCKOUT", "HIGH_STOCKOUT_RISK", "MEDIUM_STOCKOUT_RISK"])].copy()
    crit_count = len(df_stockouts[df_stockouts["risk_status"] == "CRITICAL_STOCKOUT"])
    high_count = len(df_stockouts[df_stockouts["risk_status"] == "HIGH_STOCKOUT_RISK"])
    med_count = len(df_stockouts[df_stockouts["risk_status"] == "MEDIUM_STOCKOUT_RISK"])
    lost_daily_demand = df_stockouts[df_stockouts["stock_on_hand"] == 0]["forecasted_daily_demand"].sum() if not df_stockouts.empty else 0
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f"""<div class="metric-card danger"><div><div class="metric-badge" style="color: #BE123C;">Critical Stockouts (Stock=0)</div><div class="metric-value" style="color: #BE123C;">{crit_count:,}</div></div><div class="metric-subtitle">Zero physical inventory on hand</div></div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""<div class="metric-card warning"><div><div class="metric-badge" style="color: #B45309;">High Stockout Risk</div><div class="metric-value" style="color: #B45309;">{high_count:,}</div></div><div class="metric-subtitle">Stock &lt; Safety Stock buffer</div></div>""", unsafe_allow_html=True)
    with s3:
        st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Medium Stockout Risk</div><div class="metric-value">{med_count:,}</div></div><div class="metric-subtitle">Breach within 7-day lead time</div></div>""", unsafe_allow_html=True)
    with s4:
        st.markdown(f"""<div class="metric-card danger"><div><div class="metric-badge" style="color: #BE123C;">Active Daily Lost Sales</div><div class="metric-value" style="color: #BE123C;">{lost_daily_demand:,.0f}</div></div><div class="metric-subtitle">Expected units/day unfulfilled</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("#### **Top 10 Stores Facing Critical Stockouts**")
        if not df_stockouts.empty and crit_count > 0:
            st_so = df_stockouts[df_stockouts["risk_status"] == "CRITICAL_STOCKOUT"].groupby(["store_id", "city", "store_type"]).agg(Stockout_SKUs=("sku_id", "count")).reset_index().sort_values("Stockout_SKUs", ascending=False).head(10)
            fig_st_so = px.bar(st_so, x="Stockout_SKUs", y="store_id", orientation="h", color="store_type", color_discrete_sequence=["#E11D48", "#F59E0B", "#2563EB", "#059669"])
            fig_st_so = apply_chart_theme(fig_st_so, height=300)
            fig_st_so.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_st_so, width="stretch")
        else:
            st.info("No critical stockouts found.")
    with sc2:
        st.markdown("#### **Stockout Risk Breakdown by Department**")
        if not df_stockouts.empty:
            cat_so = df_stockouts.groupby(["category", "risk_status"]).size().reset_index(name="Positions")
            fig_cat_so = px.bar(cat_so, x="category", y="Positions", color="risk_status", color_discrete_map=COLOR_MAP, barmode="stack")
            fig_cat_so = apply_chart_theme(fig_cat_so, height=300)
            fig_cat_so.update_layout(xaxis=dict(tickangle=-30), legend=dict(orientation="h", y=1.15, x=0))
            st.plotly_chart(fig_cat_so, width="stretch")
        else:
            st.info("No stockouts matching filters.")

    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("#### **Prescriptive Replenishment Worklist (Sorted by Sales Velocity)**")
    if not df_stockouts.empty:
        df_stockouts["suggested_po_qty"] = np.ceil((df_stockouts["safety_stock"] + df_stockouts["forecast_14d_demand"]) - df_stockouts["stock_on_hand"]).astype(int)
        stockout_cols = ["store_id", "city", "sku_id", "sku_name", "category", "stock_on_hand", "safety_stock", "forecasted_daily_demand", "days_of_supply", "suggested_po_qty", "risk_status", "recommended_action"]
        st.dataframe(df_stockouts[stockout_cols].sort_values("forecasted_daily_demand", ascending=False).head(150), width="stretch", hide_index=True)

# -------------------------------------------------------------
# 8. PAGE 3: OVERSTOCK / SLOW MOVERS
# -------------------------------------------------------------
elif page == "3. Overstock / Slow Movers":
    st.markdown("## **Overstock & Slow-Mover Capital Optimization**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Identify trapped working capital, stagnant inventory, and candidates for clearance markdowns.</p>", unsafe_allow_html=True)
    
    df_overstock = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_OVERSTOCK", "HIGH_OVERSTOCK", "MEDIUM_OVERSTOCK"])].copy()
    crit_ov = len(df_overstock[df_overstock["risk_status"] == "CRITICAL_OVERSTOCK"])
    high_ov = len(df_overstock[df_overstock["risk_status"] == "HIGH_OVERSTOCK"])
    med_ov = len(df_overstock[df_overstock["risk_status"] == "MEDIUM_OVERSTOCK"])
    trapped_capital = df_overstock["inventory_value_cost"].sum() if not df_overstock.empty else 0
    
    o1, o2, o3, o4 = st.columns(4)
    with o1:
        st.markdown(f"""<div class="metric-card danger"><div><div class="metric-badge" style="color: #6B21A8;">Critical Dead Stock</div><div class="metric-value" style="color: #6B21A8;">{crit_ov:,}</div></div><div class="metric-subtitle">DOS &gt; 120d + Stale Restock (&gt;90d)</div></div>""", unsafe_allow_html=True)
    with o2:
        st.markdown(f"""<div class="metric-card warning"><div><div class="metric-badge" style="color: #1D4ED8;">High Overstock</div><div class="metric-value" style="color: #1D4ED8;">{high_ov:,}</div></div><div class="metric-subtitle">DOS &gt; 90 days of supply</div></div>""", unsafe_allow_html=True)
    with o3:
        st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Medium Overstock</div><div class="metric-value">{med_ov:,}</div></div><div class="metric-subtitle">45d &lt; DOS &le; 90d</div></div>""", unsafe_allow_html=True)
    with o4:
        st.markdown(f"""<div class="metric-card warning"><div><div class="metric-badge" style="color: #B45309;">Total Trapped Capital</div><div class="metric-value" style="color: #B45309;">Rs. {trapped_capital/1e6:,.1f}M</div></div><div class="metric-subtitle">Excess cost-basis capital tied up</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    oc1, oc2 = st.columns(2)
    with oc1:
        st.markdown("#### **Trapped Working Capital by Merchandise Department**")
        if not df_overstock.empty:
            cat_ov = df_overstock.groupby("category").agg(Trapped_Capital=("inventory_value_cost", "sum")).reset_index().sort_values("Trapped_Capital", ascending=True)
            fig_cat_ov = px.bar(cat_ov, x="Trapped_Capital", y="category", orientation="h", text=cat_ov["Trapped_Capital"].apply(lambda v: f"Rs. {v/1e6:,.1f}M"))
            fig_cat_ov.update_traces(marker_color="#2563EB", textposition="outside", textfont=dict(color="#0F172A", size=11, family="Outfit"), hovertemplate="<b>%{y}</b><br>Trapped: Rs. %{x:,.0f}<extra></extra>")
            fig_cat_ov = apply_chart_theme(fig_cat_ov, height=310)
            st.plotly_chart(fig_cat_ov, width="stretch")
    with oc2:
        st.markdown("#### **Staleness Profile (Days of Supply vs. Restock Recency)**")
        if not df_overstock.empty:
            fig_scatter = px.scatter(df_overstock.head(1000), x="days_since_last_restock", y="days_of_supply", color="risk_status", size="inventory_value_cost", color_discrete_map=COLOR_MAP)
            fig_scatter = apply_chart_theme(fig_scatter, height=310)
            st.plotly_chart(fig_scatter, width="stretch")

    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.markdown("#### **Dead Stock & Clearance Markdown Candidates**")
    if not df_overstock.empty:
        overstock_cols = ["store_id", "sku_id", "sku_name", "category", "stock_on_hand", "days_since_last_restock", "forecasted_daily_demand", "days_of_supply", "inventory_value_cost", "risk_status", "recommended_action"]
        st.dataframe(df_overstock[overstock_cols].sort_values("inventory_value_cost", ascending=False).head(150), width="stretch", hide_index=True)

# -------------------------------------------------------------
# 9. PAGE 4: DEMAND FORECAST
# -------------------------------------------------------------
elif page == "4. Demand Forecast":
    st.markdown("## **Machine Learning Demand Forecasting Engine**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Multi-horizon predictive modeling powered by LightGBM Regressor (Model 2).</p>", unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Model Engine</div><div class="metric-value" style="font-size: 1.55rem;">LightGBM GBDT</div></div><div class="metric-subtitle">Optimized L2 Loss ({model_meta.get('n_trees', 70)} Trees)</div></div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card success"><div><div class="metric-badge" style="color: #047857;">Test Set WAPE</div><div class="metric-value" style="color: #047857;">{model_meta.get('test_wape', 42.16)}%</div></div><div class="metric-subtitle"><b>&plus;{model_meta.get('wape_gain_pct', 11.3)}%</b> gain over Baseline</div></div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card success"><div><div class="metric-badge" style="color: #047857;">Test Set RMSE</div><div class="metric-value" style="color: #047857;">{model_meta.get('test_rmse', 1.183)}</div></div><div class="metric-subtitle"><b>&plus;{model_meta.get('rmse_gain_pct', 20.3)}%</b> variance reduction</div></div>""", unsafe_allow_html=True)
    with m4:
        st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Network Forecast Bias</div><div class="metric-value">{model_meta.get('test_bias', -0.01)}%</div></div><div class="metric-subtitle">Unbiased network replenishment</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    st.markdown("#### **Interactive Time-Series Forecast Explorer (Test Period: H2 2025)**")
    
    if not df_ts.empty:
        fc1, fc2 = st.columns([0.85, 2.15])
        with fc1:
            avail_stores = sorted(df_ts["store_id"].unique().tolist())
            sel_ts_store = st.selectbox("Select Store", avail_stores, index=0)
            avail_skus = sorted(df_ts[df_ts["store_id"] == sel_ts_store]["sku_id"].unique().tolist())
            sel_ts_sku = st.selectbox("Select SKU", avail_skus, index=0)
            sku_name_match = df_inv[df_inv["sku_id"] == sel_ts_sku]["sku_name"].values if not df_inv.empty else []
            sku_name_str = sku_name_match[0] if len(sku_name_match) > 0 else sel_ts_sku
            st.markdown(f"""<div class="alert-box"><b>Active SKU Profile</b><br>• <b>ID:</b> <code>{sel_ts_sku}</code><br>• <b>Name:</b> {sku_name_str}<br>• <b>Location:</b> Store {sel_ts_store}</div>""", unsafe_allow_html=True)
            show_baselines = st.checkbox("Show Heuristic Baselines (SMA 28 & Lag 7)", value=True)

        with fc2:
            node_ts = df_ts[(df_ts["store_id"] == sel_ts_store) & (df_ts["sku_id"] == sel_ts_sku)].sort_values("date")
            fig_ts = go.Figure()
            fig_ts.add_trace(go.Scatter(x=node_ts["date"], y=node_ts["daily_quantity"], mode="lines+markers", name="Actual Daily Demand", line=dict(color="#0F172A", width=2), marker=dict(size=4)))
            fig_ts.add_trace(go.Scatter(x=node_ts["date"], y=node_ts["forecasted_demand"], mode="lines", name="LightGBM ML Forecast", line=dict(color="#2563EB", width=2.5)))
            if show_baselines:
                fig_ts.add_trace(go.Scatter(x=node_ts["date"], y=node_ts["baseline_sma28"], mode="lines", name="28d Rolling SMA Baseline", line=dict(color="#059669", width=1.5, dash="dash")))
                fig_ts.add_trace(go.Scatter(x=node_ts["date"], y=node_ts["baseline_lag7"], mode="lines", name="Lag-7 Seasonal Baseline", line=dict(color="#D97706", width=1.2, dash="dot")))
            fig_ts = apply_chart_theme(fig_ts, height=350)
            st.plotly_chart(fig_ts, width="stretch")

    st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    if not df_feat.empty:
        st.markdown("#### **Top 15 Machine Learning Demand Drivers (Gain Feature Importance)**")
        fig_feat = px.bar(df_feat.head(15).sort_values("Importance", ascending=True), x="Importance", y="Feature", orientation="h", text="Importance")
        fig_feat.update_traces(marker_color="#2563EB", textposition="outside", textfont=dict(color="#0F172A", size=11, family="Outfit"))
        fig_feat = apply_chart_theme(fig_feat, height=340)
        st.plotly_chart(fig_feat, width="stretch")

# -------------------------------------------------------------
# 10. PAGE 5: INVENTORY EXPLORER
# -------------------------------------------------------------
elif page == "5. Inventory Explorer":
    st.markdown("## **Inventory Explorer & Operational Action Center**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Search, inspect, and export SKU-level inventory positions and prescriptive actions.</p>", unsafe_allow_html=True)
    
    search_query = st.text_input("🔍 Search by SKU Name, SKU ID, or Brand", placeholder="Type product name, SKU ID, or brand...")
    df_exp = df_filtered.copy()
    if search_query:
        mask = (df_exp["sku_name"].str.contains(search_query, case=False, na=False) | df_exp["sku_id"].str.contains(search_query, case=False, na=False) | df_exp["brand"].str.contains(search_query, case=False, na=False))
        df_exp = df_exp[mask]

    st.markdown(f"Displaying **{len(df_exp):,}** inventory positions matching active filters.")
    exp_cols = ["store_id", "city", "sku_id", "sku_name", "category", "brand", "stock_on_hand", "safety_stock", "forecasted_daily_demand", "days_of_supply", "days_since_last_restock", "inventory_value_cost", "risk_status", "risk_reason", "recommended_action"]
    
    csv_data = df_exp[exp_cols].to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Filtered Worklist to CSV", data=csv_data, file_name="foresight_inventory_action_worklist.csv", mime="text/csv")
    st.dataframe(df_exp[exp_cols].head(300), width="stretch", hide_index=True)

# -------------------------------------------------------------
# 11. PAGE 6: PRIORITY ACTION CENTER
# -------------------------------------------------------------
elif page == "6. Priority Action Center":
    st.markdown("## **Priority Operational Action Center**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Automated prescriptive worklists categorized by operational urgency and business impact.</p>", unsafe_allow_html=True)
    
    action_tab1, action_tab2, action_tab3, action_tab4 = st.tabs([
        "🚨 1. Immediate Replenishment (Stockout)",
        "⚠️ 2. Stockout Prevention (Low Buffer)",
        "🏷️ 3. Dead Stock Clearance",
        "🔄 4. Inter-Store Transfers"
    ])
    
    with action_tab1:
        st.markdown("#### **Priority 1: Emergency Purchase Orders (Stock = 0)**")
        df_act1 = df_filtered[df_filtered["risk_status"] == "CRITICAL_STOCKOUT"].copy()
        if not df_act1.empty:
            df_act1["suggested_po_qty"] = np.ceil(df_act1["safety_stock"] + df_act1["forecast_14d_demand"]).astype(int)
            df_act1["est_lost_revenue_7d"] = df_act1["forecast_7d_demand"] * df_act1["unit_price"]
            cols1 = ["store_id", "city", "sku_id", "sku_name", "category", "forecasted_daily_demand", "suggested_po_qty", "est_lost_revenue_7d", "recommended_action"]
            disp1 = df_act1[cols1].sort_values("est_lost_revenue_7d", ascending=False)
            
            st.download_button("📥 Export Emergency PO Worklist", data=disp1.to_csv(index=False).encode('utf-8'), file_name="emergency_po_worklist.csv", mime="text/csv")
            st.dataframe(disp1.head(150), width="stretch", hide_index=True, column_config={
                "forecasted_daily_demand": st.column_config.NumberColumn("Daily Sales Velocity", format="%.2f units"),
                "suggested_po_qty": st.column_config.NumberColumn("Required PO Qty", format="%d units"),
                "est_lost_revenue_7d": st.column_config.NumberColumn("7-Day Revenue at Risk", format="Rs. %,.0f")
            })
        else:
            st.success("No immediate zero-stock emergencies matching filters!")

    with action_tab2:
        st.markdown("#### **Priority 2: Preemptive Reorders (Stock Below Safety Buffer)**")
        df_act2 = df_filtered[df_filtered["risk_status"] == "HIGH_STOCKOUT_RISK"].copy()
        if not df_act2.empty:
            df_act2["suggested_po_qty"] = np.ceil((df_act2["safety_stock"] + df_act2["forecast_14d_demand"]) - df_act2["stock_on_hand"]).astype(int)
            cols2 = ["store_id", "city", "sku_id", "sku_name", "stock_on_hand", "safety_stock", "days_of_supply", "suggested_po_qty", "recommended_action"]
            disp2 = df_act2[cols2].sort_values("days_of_supply", ascending=True)
            
            st.download_button("📥 Export Preemptive Reorder List", data=disp2.to_csv(index=False).encode('utf-8'), file_name="preemptive_reorders.csv", mime="text/csv")
            st.dataframe(disp2.head(150), width="stretch", hide_index=True, column_config={
                "days_of_supply": st.column_config.NumberColumn("Days Left", format="%.1f d"),
                "suggested_po_qty": st.column_config.NumberColumn("PO Quantity", format="%d units")
            })
        else:
            st.info("No preemptive reorder triggers matching filters.")

    with action_tab3:
        st.markdown("#### **Priority 3: Trapped Capital Clearance Candidates (DOS > 120 Days)**")
        df_act3 = df_filtered[df_filtered["risk_status"] == "CRITICAL_OVERSTOCK"].copy()
        if not df_act3.empty:
            df_act3["recommended_markdown_discount"] = "25% - 35% Off Flash Clearance"
            cols3 = ["store_id", "city", "sku_id", "sku_name", "stock_on_hand", "days_since_last_restock", "days_of_supply", "inventory_value_cost", "recommended_markdown_discount", "recommended_action"]
            disp3 = df_act3[cols3].sort_values("inventory_value_cost", ascending=False)
            
            st.download_button("📥 Export Clearance Action List", data=disp3.to_csv(index=False).encode('utf-8'), file_name="dead_stock_clearance.csv", mime="text/csv")
            st.dataframe(disp3.head(150), width="stretch", hide_index=True, column_config={
                "inventory_value_cost": st.column_config.NumberColumn("Trapped Capital", format="Rs. %,.0f"),
                "days_of_supply": st.column_config.NumberColumn("Days Supply", format="%.0f d")
            })
        else:
            st.info("No critical dead stock matching filters.")

    with action_tab4:
        st.markdown("#### **Priority 4: Inter-Store Inventory Transfer Optimization**")
        st.markdown("<p style='color: #475569; font-size: 0.9rem;'>Automatically match stores with <b>0 stock</b> against network stores carrying <b>excess inventory (&gt;90 DOS)</b> for the exact same SKU.</p>", unsafe_allow_html=True)
        
        stockout_skus = set(df_inv[df_inv["stock_on_hand"] == 0]["sku_id"].unique())
        overstock_skus = set(df_inv[df_inv["days_of_supply"] > 90]["sku_id"].unique())
        transfer_skus = stockout_skus.intersection(overstock_skus)
        
        transfer_records = []
        for s in list(transfer_skus)[:50]:
            dest_nodes = df_inv[(df_inv["sku_id"] == s) & (df_inv["stock_on_hand"] == 0)]
            src_nodes = df_inv[(df_inv["sku_id"] == s) & (df_inv["days_of_supply"] > 90)]
            if not dest_nodes.empty and not src_nodes.empty:
                dest_row = dest_nodes.iloc[0]
                src_row = src_nodes.sort_values("stock_on_hand", ascending=False).iloc[0]
                transfer_qty = min(int(src_row["stock_on_hand"] * 0.4), int(dest_row["forecast_14d_demand"] + dest_row["safety_stock"]))
                if transfer_qty > 0:
                    transfer_records.append({
                        "SKU_ID": s,
                        "Product_Name": dest_row["sku_name"],
                        "Category": dest_row["category"],
                        "Source_Store": f"{src_row['store_id']} ({src_row['city']})",
                        "Source_Stock": int(src_row["stock_on_hand"]),
                        "Source_DOS": f"{src_row['days_of_supply']:.0f}d",
                        "Destination_Store": f"{dest_row['store_id']} ({dest_row['city']})",
                        "Destination_Stock": 0,
                        "Transfer_Quantity": transfer_qty,
                        "Action": f"Transfer {transfer_qty} units from {src_row['store_id']} to {dest_row['store_id']}"
                    })
        if transfer_records:
            df_trans = pd.DataFrame(transfer_records)
            st.download_button("📥 Export Inter-Store Transfer Worklist", data=df_trans.to_csv(index=False).encode('utf-8'), file_name="inter_store_transfers.csv", mime="text/csv")
            st.dataframe(df_trans, width="stretch", hide_index=True)
        else:
            st.info("No inter-store transfer matches found.")

# -------------------------------------------------------------
# 12. PAGE 7: WHAT-IF INVENTORY SIMULATOR
# -------------------------------------------------------------
elif page == "7. What-If Simulator":
    st.markdown("## **What-If Inventory Scenario Simulator**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Simulate supply chain parameter adjustments and observe resulting Days of Supply and risk classifications in real time.</p>", unsafe_allow_html=True)
    
    sim_col1, sim_col2 = st.columns([1, 1.2])
    
    with sim_col1:
        st.markdown("#### **1. Configure Simulation Parameters**")
        sim_store = st.selectbox("Select Store Location", sorted(df_inv["store_id"].unique().tolist()), index=0)
        sim_skus = sorted(df_inv[df_inv["store_id"] == sim_store]["sku_id"].unique().tolist())
        sim_sku = st.selectbox("Select Product SKU", sim_skus, index=0)
        
        base_node = df_inv[(df_inv["store_id"] == sim_store) & (df_inv["sku_id"] == sim_sku)].iloc[0]
        st.markdown(f"""<div class="alert-box"><b>Selected Item:</b> {base_node['sku_name']}<br>• Category: {base_node['category']} | Price: Rs. {base_node['unit_price']:.1f}</div>""", unsafe_allow_html=True)
        
        st.markdown("**Simulated Inputs:**")
        sim_stock = st.slider("Simulated Physical Stock on Hand (Units)", min_value=0, max_value=int(max(base_node["stock_on_hand"] * 2, 500)), value=int(base_node["stock_on_hand"]))
        sim_demand = st.slider("Expected Daily Demand Rate (Units/Day)", min_value=0.1, max_value=float(max(base_node["forecasted_daily_demand"] * 3, 20.0)), value=float(base_node["forecasted_daily_demand"]), step=0.1)
        sim_lead_time = st.slider("Vendor Replenishment Lead Time (Days)", min_value=1, max_value=30, value=7)
        sim_safety = st.slider("Safety Stock Buffer (Units)", min_value=1, max_value=int(base_node["safety_stock"] * 2 + 10), value=int(base_node["safety_stock"]))
        sim_reorder_point = st.number_input("Reorder Point Threshold (Units)", min_value=1, value=int(base_node["reorder_point"]))

    with sim_col2:
        st.markdown("#### **2. Real-Time Risk Simulation Output**")
        sim_f_lead = sim_demand * sim_lead_time
        sim_dos = (sim_stock / sim_demand) if sim_demand > 0 else 999.0
        
        if sim_stock == 0:
            sim_status = "CRITICAL_STOCKOUT"
            sim_color = "#E11D48"
            sim_rec = "Emergency Expedited PO Required Immediately"
        elif sim_stock < sim_safety:
            sim_status = "HIGH_STOCKOUT_RISK"
            sim_color = "#F43F5E"
            sim_rec = "Urgent Purchase Order Reorder"
        elif sim_stock < (sim_f_lead + sim_safety):
            sim_status = "MEDIUM_STOCKOUT_RISK"
            sim_color = "#FDA4AF"
            sim_rec = "Standard Lead-Time Reorder PO"
        elif sim_dos > 120 and sim_stock >= 2.5 * sim_reorder_point:
            sim_status = "CRITICAL_OVERSTOCK"
            sim_color = "#7C3AED"
            sim_rec = "Execute Clearance Markdown Campaign"
        elif sim_dos > 90 or sim_stock >= 2.5 * sim_reorder_point:
            sim_status = "HIGH_OVERSTOCK"
            sim_color = "#2563EB"
            sim_rec = "Freeze PO & Reallocate Inventory"
        elif sim_dos > 45:
            sim_status = "MEDIUM_OVERSTOCK"
            sim_color = "#60A5FA"
            sim_rec = "Reduce Next Cycle Order Quantity"
        else:
            sim_status = "HEALTHY_OPTIMAL"
            sim_color = "#059669"
            sim_rec = "Maintain Routine Scheduled Monitoring"
            
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""<div class="metric-card" style="border-top: 5px solid {sim_color};"><div><div class="metric-badge">Simulated Risk Status</div><div class="metric-value" style="font-size: 1.35rem; color: {sim_color};">{sim_status}</div></div><div class="metric-subtitle">Action: <b>{sim_rec}</b></div></div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""<div class="metric-card primary"><div><div class="metric-badge">Simulated Days of Supply</div><div class="metric-value">{sim_dos:.1f} Days</div></div><div class="metric-subtitle">Lead-Time Demand: <b>{sim_f_lead:.1f} units</b></div></div>""", unsafe_allow_html=True)
            
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=sim_dos,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Days of Supply (DOS) Coverage", 'font': {'size': 14, 'family': 'Outfit'}},
            delta={'reference': base_node['days_of_supply'], 'increasing': {'color': "#2563EB"}, 'decreasing': {'color': "#E11D48"}},
            gauge={
                'axis': {'range': [None, max(150, sim_dos * 1.2)], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
                'bar': {'color': sim_color},
                'bgcolor': "#FFFFFF",
                'borderwidth': 1,
                'bordercolor': "#E2E8F0",
                'steps': [
                    {'range': [0, 7], 'color': "#FFE4E6"},
                    {'range': [7, 45], 'color': "#D1FAE5"},
                    {'range': [45, 90], 'color': "#FEF3C7"},
                    {'range': [90, 150], 'color': "#EDE9FE"}
                ],
                'threshold': {'line': {'color': "#0F172A", 'width': 3}, 'thickness': 0.75, 'value': 45}
            }
        ))
        fig_gauge = apply_chart_theme(fig_gauge, height=280)
        st.plotly_chart(fig_gauge, width="stretch")

# -------------------------------------------------------------
# 13. PAGE 8: INTELLIGENCE ASSISTANT (DATA-GROUNDED AI)
# -------------------------------------------------------------
elif page == "8. Intelligence Assistant":
    st.markdown("## **FORESIGHT Intelligence Assistant**")
    st.markdown("<p style='color: #475569; font-size: 1.0rem; margin-top: -6px; margin-bottom: 20px;'>Ask questions to explore project datasets, risk classifications, and replenishment recommendations.</p>", unsafe_allow_html=True)
    
    st.markdown("#### **Quick Business Questions:**")
    qc1, qc2, qc3, qc4, qc5 = st.columns(5)
    q_selected = None
    if qc1.button("🚨 Highest Stockout Risk"):
        q_selected = "Which SKUs have the highest stockout risk?"
    if qc2.button("💰 Most Trapped Capital"):
        q_selected = "Which inventory has the most trapped capital?"
    if qc3.button("📦 What to Replenish First"):
        q_selected = "What should I replenish first?"
    if qc4.button("🏷️ Overstock by Category"):
        q_selected = "Which categories have the most overstock?"
    if qc5.button("🏢 Riskiest Store Locations"):
        q_selected = "Which stores have the highest stockout deficit?"

    user_query = st.text_input("💬 Ask a question about NorthBay Living's inventory and forecasts:", value=q_selected if q_selected else "", placeholder="e.g. Which SKUs have zero stock? What is the trapped capital in Personal Care?")
    
    if user_query:
        q_lower = user_query.lower()
        st.markdown(f"""<div class="chat-user">User: {user_query}</div>""", unsafe_allow_html=True)
        
        with st.spinner("Analyzing verified project outputs..."):
            if "stockout" in q_lower or "zero stock" in q_lower or "shortage" in q_lower:
                crit_nodes = df_filtered[df_filtered["risk_status"] == "CRITICAL_STOCKOUT"]
                lost_rev = (crit_nodes["forecast_7d_demand"] * crit_nodes["unit_price"]).sum()
                top_items = crit_nodes.sort_values("forecasted_daily_demand", ascending=False).head(5)
                
                st.markdown(f"""
                <div class="chat-assistant">
                <b>Analysis Result: Stockout Deficit</b><br>
                • Found <b>{len(crit_nodes):,}</b> active positions with zero physical stock in the filtered selection.<br>
                • <b>7-Day Estimated Revenue at Risk:</b> Rs. {lost_rev:,.0f}<br>
                • <b>Top Immediate Deficits:</b>
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(top_items[["store_id", "city", "sku_id", "sku_name", "category", "forecasted_daily_demand", "safety_stock", "recommended_action"]], width="stretch", hide_index=True)
                
            elif "trapped" in q_lower or "capital" in q_lower or "overstock" in q_lower or "dead stock" in q_lower:
                over_nodes = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_OVERSTOCK", "HIGH_OVERSTOCK", "MEDIUM_OVERSTOCK"])]
                trapped_cost = over_nodes["inventory_value_cost"].sum()
                top_cat_trap = over_nodes.groupby("category")["inventory_value_cost"].sum().sort_values(ascending=False).head(5)
                
                st.markdown(f"""
                <div class="chat-assistant">
                <b>Analysis Result: Trapped Working Capital</b><br>
                • Total capital tied up in excess inventory: <b>Rs. {trapped_cost/1e6:,.1f} Million</b> ({len(over_nodes):,} positions).<br>
                • <b>Top Categories by Trapped Capital:</b><br>
                { "<br>".join([f"&bull; <b>{cat}:</b> Rs. {val/1e6:,.2f}M" for cat, val in top_cat_trap.items()]) }
                </div>
                """, unsafe_allow_html=True)
                
            elif "replenish" in q_lower or "order" in q_lower or "po" in q_lower:
                reorder_nodes = df_filtered[df_filtered["risk_status"].isin(["CRITICAL_STOCKOUT", "HIGH_STOCKOUT_RISK"])].copy()
                reorder_nodes["suggested_po"] = np.ceil((reorder_nodes["safety_stock"] + reorder_nodes["forecast_14d_demand"]) - reorder_nodes["stock_on_hand"]).astype(int)
                top_po = reorder_nodes.sort_values("forecasted_daily_demand", ascending=False).head(10)
                
                st.markdown(f"""
                <div class="chat-assistant">
                <b>Prescriptive Replenishment Recommendations:</b><br>
                • <b>{len(reorder_nodes):,}</b> positions require immediate replenishment orders to prevent stockouts.<br>
                • Priority ranking is calculated based on daily forecast velocity and safety stock buffers:
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(top_po[["store_id", "city", "sku_id", "sku_name", "stock_on_hand", "safety_stock", "forecasted_daily_demand", "suggested_po", "recommended_action"]], width="stretch", hide_index=True)
                
            elif "store" in q_lower or "location" in q_lower or "city" in q_lower:
                store_so = df_filtered[df_filtered["stock_on_hand"] == 0].groupby(["store_id", "city", "store_type"]).agg(Zero_Stock_SKUs=("sku_id", "count")).reset_index().sort_values("Zero_Stock_SKUs", ascending=False).head(5)
                
                st.markdown(f"""
                <div class="chat-assistant">
                <b>Store Location Risk Analysis:</b><br>
                • Stores with the highest number of stockout positions:
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(store_so, width="stretch", hide_index=True)
                
            else:
                st.markdown(f"""
                <div class="chat-assistant">
                <b>Executive Summary:</b><br>
                • <b>Network Capital:</b> Rs. {df_filtered['inventory_value_cost'].sum()/1e6:,.1f}M across {len(df_filtered):,} active nodes.<br>
                • <b>Stockout Positions:</b> {len(df_filtered[df_filtered['risk_status'].str.contains('STOCKOUT')]):,} positions.<br>
                • <b>Overstock Positions:</b> {len(df_filtered[df_filtered['risk_status'].str.contains('OVERSTOCK')]):,} positions.<br>
                • <i>Try asking about specific stockouts, trapped capital, replenishment orders, or store risks!</i>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr style='margin: 24px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
    
    st.markdown("#### **Single-Item 'Explain This Risk' Diagnostic Tool**")
    d_c1, d_c2 = st.columns([1, 2])
    with d_c1:
        insp_store = st.selectbox("Inspector Store", sorted(df_inv["store_id"].unique().tolist()), key="insp_st")
        insp_skus = sorted(df_inv[df_inv["store_id"] == insp_store]["sku_id"].unique().tolist())
        insp_sku = st.selectbox("Inspector SKU", insp_skus, key="insp_sk")
    
    with d_c2:
        insp_row = df_inv[(df_inv["store_id"] == insp_store) & (df_inv["sku_id"] == insp_sku)].iloc[0]
        st.markdown(f"""
        <div class="alert-box" style="border-left-color: {COLOR_MAP.get(insp_row['risk_status'], '#2563EB')};">
        <b>Diagnostic Assessment for {insp_row['sku_name']} (Store {insp_row['store_id']}, {insp_row['city']}):</b><br>
        • <b>Risk Classification:</b> <span style="font-weight:700; color:{COLOR_MAP.get(insp_row['risk_status'], '#0F172A')};">{insp_row['risk_status']}</span><br>
        • <b>Physical Stock:</b> {insp_row['stock_on_hand']} units | <b>Safety Buffer:</b> {insp_row['safety_stock']} units | <b>Reorder Point:</b> {insp_row['reorder_point']} units<br>
        • <b>Forecast Daily Velocity:</b> {insp_row['forecasted_daily_demand']:.2f} units/day | <b>Days of Supply:</b> {insp_row['days_of_supply']:.1f} days<br>
        • <b>Staleness Recency:</b> {insp_row['days_since_last_restock']} days since last restock<br>
        • <b>Explainable Decision Rule:</b> {insp_row['risk_reason']}<br>
        • <b>Prescriptive Action:</b> <b>{insp_row['recommended_action']}</b>
        </div>
        """, unsafe_allow_html=True)
