"""
inventory.py — Streamlit Inventory Analysis tab component for the Local Shop Assistant.

Renders:
  - A colour-coded stock table (rows below threshold highlighted in light red)
  - A horizontal bar chart showing current stock levels with a threshold line
  - A note about data freshness
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src import analysis


def render_inventory(df: pd.DataFrame, min_threshold: int) -> None:
    """
    Render the Inventory Analysis tab.

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned sales/stock DataFrame produced by data_loader.load_data().
    min_threshold : int
        Minimum stock level set by the user in the sidebar.  Rows below this
        value are highlighted and bars are coloured red in the chart.
    """

    st.header("📦 Inventory Levels")

    # ------------------------------------------------------------------ #
    # SECTION 1 — Colour-coded stock table                                #
    # ------------------------------------------------------------------ #
    # get_current_stock returns: item_name, category, current_stock
    # current_stock is the stock_remaining from the LAST recorded row per item.
    stock_df = analysis.get_current_stock(df)

    st.subheader("Current Stock Levels")

    # Build a pandas Styler that highlights low-stock rows in light red so
    # the shopkeeper can spot problems at a glance without reading every number.
    def highlight_low_stock(row: pd.Series) -> list[str]:
        """Return red background style for every cell in rows below threshold."""
        if row["current_stock"] < min_threshold:
            return ["background-color: #FFCCCC"] * len(row)
        return [""] * len(row)

    # Rename columns to friendly display names before applying the styler.
    display_stock = stock_df.rename(
        columns={
            "item_name": "Product",
            "category": "Category",
            "current_stock": "Stock Remaining",
        }
    )

    styled = display_stock.style.apply(highlight_low_stock, axis=1)
    st.dataframe(styled, use_container_width=True, hide_index=True)

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 2 — Horizontal bar chart of current stock levels            #
    # ------------------------------------------------------------------ #
    st.subheader("Stock Level Chart")

    # Colour each bar green (safe) or red (below threshold) for quick scanning.
    bar_colours = [
        "red" if stock < min_threshold else "green"
        for stock in stock_df["current_stock"]
    ]

    fig, ax = plt.subplots(figsize=(9, max(4, len(stock_df) * 0.6)))

    ax.barh(stock_df["item_name"], stock_df["current_stock"], color=bar_colours)

    # Draw a vertical dashed red line at the minimum threshold value.
    ax.axvline(
        x=min_threshold,
        color="red",
        linestyle="--",
        linewidth=1.5,
        label=f"Min threshold ({min_threshold})",
    )

    ax.legend(loc="lower right")
    ax.set_xlabel("Units in Stock")
    ax.set_title("Current Stock Levels")
    ax.invert_yaxis()  # keep the same top-to-bottom order as the table
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)  # release memory after rendering

    # ------------------------------------------------------------------ #
    # SECTION 3 — Data freshness note                                     #
    # ------------------------------------------------------------------ #
    st.caption(
        "ℹ️ Stock levels reflect the last recorded entry per item in the CSV."
    )
