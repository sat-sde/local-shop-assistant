"""
app.py — Main entry point for the Local Shop Stock & Sales Assistant.

A Streamlit application designed for small kirana store owners to track
sales, monitor inventory levels, and get data-driven restock suggestions.
"""

import streamlit as st
import pandas as pd

# ── Src module imports ────────────────────────────────────────────────────────
from src import data_loader, analysis
from src.components import dashboard, sales, inventory, restock

# ── Page configuration (must be the first Streamlit call) ────────────────────
st.set_page_config(
    title="Local Shop Assistant",
    page_icon="🛒",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Settings & file upload
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")

    # File uploader — accepts CSV only
    uploaded_file = st.file_uploader(
        label="Upload your sales CSV",
        type=["csv"],
        help="Upload a CSV file matching the required column format.",
    )

    # Hint shown when no file is uploaded
    st.markdown(
        "_No file uploaded? The app loads the default data from "
        "`data/raw/stock_sales_raw.csv`_"
    )

    st.divider()

    # Minimum stock threshold — items below this are flagged as low stock
    min_threshold = st.number_input(
        label="Minimum stock threshold (units)",
        min_value=1,
        max_value=100,
        value=10,
        step=1,
        help="Items with stock below this number will be highlighted as low.",
    )

    # Supplier lead time — used in restock quantity calculation
    lead_days = st.number_input(
        label="Supplier lead time (days)",
        min_value=1,
        max_value=30,
        value=3,
        step=1,
        help="Number of days until your next supplier delivery.",
    )

    st.markdown("---")

    # Show which data source is active
    if uploaded_file is not None:
        data_source_label = uploaded_file.name
    else:
        data_source_label = "Default CSV"

    st.markdown(f"📂 **Data source:** {data_source_label}")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA — Title, disclosure, data loading, tabs
# ─────────────────────────────────────────────────────────────────────────────

# App title and subtitle
st.title("🛒 Local Shop Stock & Sales Assistant")
st.markdown("_Built for small kirana stores · Data-driven, not guesswork_")

# Disclosure banner — clarifies that sample data is synthetic
st.info(
    "ℹ️ This application uses synthetic sample data representative of a small "
    "Indian kirana store. No real shopkeeper data is used. Replace "
    "`data/raw/stock_sales_raw.csv` with your own CSV to analyse real data."
)

# ── Data loading ──────────────────────────────────────────────────────────────
# Determine the data source: uploaded file or the bundled default CSV
if uploaded_file is not None:
    data_source = uploaded_file          # Streamlit UploadedFile object
else:
    data_source = "data/raw/stock_sales_raw.csv"   # Path to default CSV

# Load and validate the data; display any validation warnings
try:
    df, issues = data_loader.load_data(data_source)

    # Surface data quality warnings to the user (non-blocking)
    if issues:
        with st.expander("⚠️ Data quality notices", expanded=False):
            for issue in issues:
                st.warning(issue)

except Exception as exc:
    # Show a clear error and stop further rendering
    st.error(f"❌ Could not load data: {exc}")
    st.stop()

# ── Tab layout ────────────────────────────────────────────────────────────────
tab_dashboard, tab_sales, tab_inventory, tab_restock = st.tabs(
    ["📊 Dashboard", "📈 Sales Analysis", "📦 Inventory", "🔄 Restock Suggestions"]
)

# Dashboard tab — high-level KPI summary
with tab_dashboard:
    dashboard.render(df, min_threshold=min_threshold, lead_days=lead_days)

# Sales Analysis tab — product-level and time-series sales breakdown
with tab_sales:
    sales.render(df)

# Inventory tab — current stock levels and low-stock alerts
with tab_inventory:
    inventory.render(df, min_threshold=min_threshold)

# Restock Suggestions tab — data-driven reorder recommendations
with tab_restock:
    restock.render(df, min_threshold=min_threshold, lead_days=lead_days)
