"""
restock.py — Streamlit Restock Suggestions tab component for the Local Shop Assistant.

Renders:
  - A table of items that need restocking (empty state if none needed)
  - An expander explaining how the suggested quantities were calculated
"""

import streamlit as st
import pandas as pd

from src import analysis


def render_restock(df: pd.DataFrame, min_threshold: int, lead_days: int) -> None:
    """
    Render the Restock Suggestions tab.

    Parameters
    ----------
    df : pd.DataFrame
        The cleaned sales/stock DataFrame produced by data_loader.load_data().
    min_threshold : int
        Minimum stock level set by the user in the sidebar.
    lead_days : int
        Number of days until the next supplier delivery, set in the sidebar.
        Used as a buffer when calculating how much to reorder.
    """

    st.header("🔄 Restock Suggestions")

    # ------------------------------------------------------------------ #
    # SECTION 1 — Compute restock suggestions                             #
    # ------------------------------------------------------------------ #
    # get_restock_suggestions returns items where suggested_restock_qty > 0.
    # Columns: item_name, current_stock, avg_daily_sales,
    #          suggested_restock_qty, calculation_note
    suggestions_df = analysis.get_restock_suggestions(df, min_threshold, lead_days)

    # ------------------------------------------------------------------ #
    # SECTION 2 — Display suggestions or empty-state message              #
    # ------------------------------------------------------------------ #
    if suggestions_df.empty:
        # Nothing to restock — reassure the shopkeeper.
        st.success("No restocking needed based on current data.")
    else:
        st.markdown(
            f"**{len(suggestions_df)} item(s)** need restocking based on current "
            f"stock levels, a minimum threshold of **{min_threshold} units**, "
            f"and a lead time of **{lead_days} day(s)**."
        )

        # Rename raw column names to user-friendly display names.
        display_df = suggestions_df.rename(
            columns={
                "item_name": "Product",
                "current_stock": "Current Stock",
                "avg_daily_sales": "Avg Daily Sales",
                "suggested_restock_qty": "Suggested Restock Qty",
                "calculation_note": "How It's Calculated",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()

    # ------------------------------------------------------------------ #
    # SECTION 3 — Methodology expander                                    #
    # ------------------------------------------------------------------ #
    # Shown regardless of whether suggestions exist, so the shopkeeper can
    # always understand the logic behind the numbers.
    with st.expander("📐 How are these quantities calculated?"):
        st.markdown(
            """
**Formula:**

```
Suggested Restock = max(0, Minimum Threshold + (Avg Daily Sales × Lead Days) − Current Stock)
```

- **Minimum Threshold:** set by you in the sidebar (default: 10 units)
- **Avg Daily Sales:** total units sold ÷ number of days item appears in data
- **Lead Days:** how many days until your next supplier delivery (default: 3)
- **Current Stock:** last recorded stock_remaining from the CSV

---

**Limitation:** These suggestions are based only on the data in the CSV.
If sales patterns change (festivals, seasons, weather), the suggestions
may not reflect actual needs. Treat them as a starting point, not a guarantee.
"""
        )
