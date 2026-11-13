"""
sales.py — Streamlit Sales Analysis tab component for the Local Shop Assistant.

Renders:
  - A product-level sales summary table
  - A horizontal bar chart of revenue by product, coloured by category
  - Fast movers (top sellers) and slow movers side by side
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src import analysis


# Colour mapping for each category used in the bar chart.
# Any category not in this dict falls back to grey.
CATEGORY_COLOURS: dict[str, str] = {
    "Staples": "steelblue",
    "Snacks": "orange",
    "Household": "green",
    "Personal Care": "purple",
    "Dairy": "brown",
}
DEFAULT_COLOUR = "grey"


def render_sales(df: pd.DataFrame) -> None:
    """
    Render the Sales Analysis tab.

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned sales/stock DataFrame produced by data_loader.load_data().
    """

    st.header("🛍️ Sales Analysis")

    # ------------------------------------------------------------------ #
    # SECTION 1 — Product sales summary table                             #
    # ------------------------------------------------------------------ #
    # get_product_sales returns: item_name, category, total_units_sold,
    # total_revenue_inr — sorted by total_units_sold descending.
    product_sales = analysis.get_product_sales(df)

    st.subheader("Product Sales Summary")

    # Rename raw column names to user-friendly display names.
    display_sales = product_sales.rename(
        columns={
            "item_name": "Product",
            "category": "Category",
            "total_units_sold": "Units Sold",
            "total_revenue_inr": "Revenue (₹)",
        }
    )
    st.dataframe(display_sales, use_container_width=True, hide_index=True)

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 2 — Horizontal bar chart: Revenue by Product                #
    # ------------------------------------------------------------------ #
    st.subheader("Revenue by Product")

    # Build a colour list aligned with the product order in the DataFrame.
    bar_colours = [
        CATEGORY_COLOURS.get(cat, DEFAULT_COLOUR)
        for cat in product_sales["category"]
    ]

    fig, ax = plt.subplots(figsize=(9, max(4, len(product_sales) * 0.55)))

    bars = ax.barh(
        product_sales["item_name"],
        product_sales["total_revenue_inr"],
        color=bar_colours,
    )

    # Add value labels at the right end of each bar for easy reading.
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + (product_sales["total_revenue_inr"].max() * 0.01),  # small padding
            bar.get_y() + bar.get_height() / 2,
            f"₹{width:,.0f}",
            va="center",
            ha="left",
            fontsize=9,
        )

    ax.set_xlabel("Total Revenue (₹)")
    ax.set_title("Revenue by Product")
    ax.invert_yaxis()  # highest revenue bar at the top
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)  # release memory; prevents Streamlit from showing stale figures

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 3 — Fast movers and slow movers                             #
    # ------------------------------------------------------------------ #
    # get_fast_slow_movers returns a tuple of (fast_df, slow_df).
    fast_df, slow_df = analysis.get_fast_slow_movers(df)

    st.subheader("Top & Slow Sellers")

    col_fast, col_slow = st.columns(2)

    with col_fast:
        st.markdown("### 🏆 Top Sellers")
        display_fast = fast_df.rename(
            columns={
                "item_name": "Product",
                "category": "Category",
                "total_units_sold": "Units Sold",
                "total_revenue_inr": "Revenue (₹)",
            }
        )
        st.dataframe(display_fast, use_container_width=True, hide_index=True)

    with col_slow:
        st.markdown("### 🐢 Slow Movers")
        display_slow = slow_df.rename(
            columns={
                "item_name": "Product",
                "category": "Category",
                "total_units_sold": "Units Sold",
                "total_revenue_inr": "Revenue (₹)",
            }
        )
        st.dataframe(display_slow, use_container_width=True, hide_index=True)
