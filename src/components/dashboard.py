"""
dashboard.py — Streamlit Dashboard tab component for the Local Shop Assistant.

Renders an overview: summary metrics, low-stock warnings, and data-quality issues.
"""

import streamlit as st
import pandas as pd

from src import analysis


def render_dashboard(df: pd.DataFrame, issues: list[str]) -> None:
    """
    Render the Dashboard tab.

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned sales/stock DataFrame produced by data_loader.load_data().
    issues : list[str]
        Human-readable data-quality warnings from data_loader.load_data().
        Empty list means no issues were detected.
    """

    st.header("📊 Dashboard Overview")

    # ------------------------------------------------------------------ #
    # SECTION 1 — Summary metric cards                                     #
    # ------------------------------------------------------------------ #
    # Retrieve all headline numbers from the analysis module in one call.
    metrics = analysis.get_summary_metrics(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Revenue (₹)",
            value=f"₹{metrics['total_revenue']:,.2f}",
        )
    with col2:
        st.metric(
            label="📦 Total Units Sold",
            value=f"{metrics['total_units_sold']:,}",
        )
    with col3:
        st.metric(
            label="🛒 Products Tracked",
            value=metrics["num_products"],
        )
    with col4:
        st.metric(
            label="📅 Days Recorded",
            value=metrics["num_days"],
        )

    # Show the date range the data covers, for context.
    min_date, max_date = metrics["date_range"]
    st.caption(f"Data covers: **{min_date}** → **{max_date}**")

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 2 — Low stock alert table                                    #
    # ------------------------------------------------------------------ #
    # get_low_stock_items uses the default threshold of 10 units.
    # The sidebar controls the actual threshold used in other tabs; the
    # dashboard shows a quick-glance alert with the default so users always
    # see a warning even before they visit the Inventory tab.
    low_stock_df = analysis.get_low_stock_items(df)

    st.subheader("⚠️ Low Stock Alert")

    if low_stock_df.empty:
        # Green success banner — nothing to worry about.
        st.success("All items are adequately stocked.")
    else:
        # Red-tinted warning header to draw the shopkeeper's eye immediately.
        st.markdown(
            "<p style='color:#c0392b; font-weight:bold;'>"
            f"🔴 {len(low_stock_df)} item(s) are running low on stock!</p>",
            unsafe_allow_html=True,
        )
        # Rename columns to friendlier display names before showing the table.
        display_df = low_stock_df.rename(
            columns={
                "item_name": "Item",
                "category": "Category",
                "current_stock": "Stock Remaining",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 3 — Data quality issues expander                            #
    # ------------------------------------------------------------------ #
    # Only shown when the loader detected problems (duplicates, mismatches,
    # missing values, etc.).  Wrapped in an expander so it doesn't clutter
    # the dashboard for clean datasets.
    if issues:
        with st.expander("⚠️ Data Issues Found", expanded=False):
            st.warning(
                f"**{len(issues)} issue(s) were detected in your CSV file.**  "
                "These do not stop the app from running, but you may want to "
                "review and fix them in your data."
            )
            for i, issue in enumerate(issues, start=1):
                st.markdown(f"**{i}.** {issue}")
