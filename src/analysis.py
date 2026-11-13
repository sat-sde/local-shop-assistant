"""
analysis.py
===========
Computes all business metrics from a clean shop DataFrame produced by
``data_loader.load_data()``.

LIMITATIONS
-----------
* Restock suggestions are based solely on average daily sales over the
  observed period (at most 3 days in this dataset). Very short histories
  can produce misleading averages — a single high-demand day inflates the
  figure while a low-demand day deflates it. Treat the suggestions as a
  rough guide, not a precise ordering target.
* "Current stock" is the last recorded stock_remaining value per item.
  If the CSV is not in chronological order and contains multiple records
  per day per item, the result depends on which row pandas picks last.
  Always ensure the source data is accurate and sorted by date.
* avg_daily_sales counts only the days that an item appears in the data,
  not the total calendar span of the dataset.  Items not sold on a given
  day are not represented, so the average may be slightly optimistic.

Public API
----------
get_summary_metrics(df)        -> dict
get_product_sales(df)          -> pd.DataFrame
get_current_stock(df)          -> pd.DataFrame
get_low_stock_items(df, ...)   -> pd.DataFrame
get_restock_suggestions(df, .) -> pd.DataFrame
get_fast_slow_movers(df, ...)  -> tuple[pd.DataFrame, pd.DataFrame]
"""

import pandas as pd


# ---------------------------------------------------------------------------
# 1. Summary metrics
# ---------------------------------------------------------------------------

def get_summary_metrics(df: pd.DataFrame) -> dict:
    """Return high-level summary statistics for the entire dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.

    Returns
    -------
    dict with keys:
        total_revenue      (float)  — sum of total_inr across all rows.
        total_units_sold   (int)    — sum of quantity_sold across all rows.
        num_products       (int)    — count of unique item names.
        num_days           (int)    — count of unique dates.
        date_range         (tuple)  — (min_date_str, max_date_str).
    """

    total_revenue = float(df["total_inr"].sum())
    total_units_sold = int(df["quantity_sold"].sum())
    num_products = int(df["item_name"].nunique())
    num_days = int(df["date"].nunique())

    # Format dates as "YYYY-MM-DD" strings for easy display.
    min_date = df["date"].min()
    max_date = df["date"].max()
    date_range = (
        min_date.strftime("%Y-%m-%d") if pd.notna(min_date) else "N/A",
        max_date.strftime("%Y-%m-%d") if pd.notna(max_date) else "N/A",
    )

    return {
        "total_revenue": total_revenue,
        "total_units_sold": total_units_sold,
        "num_products": num_products,
        "num_days": num_days,
        "date_range": date_range,
    }


# ---------------------------------------------------------------------------
# 2. Product-level sales breakdown
# ---------------------------------------------------------------------------

def get_product_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by product.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.

    Returns
    -------
    pd.DataFrame
        Columns: item_name, category, total_units_sold, total_revenue_inr.
        Sorted by total_units_sold descending (best-seller first).
    """

    grouped = (
        df.groupby(["item_name", "category"], as_index=False)
        .agg(
            total_units_sold=("quantity_sold", "sum"),
            total_revenue_inr=("total_inr", "sum"),
        )
        .sort_values("total_units_sold", ascending=False)
        .reset_index(drop=True)
    )

    return grouped


# ---------------------------------------------------------------------------
# 3. Current stock levels
# ---------------------------------------------------------------------------

def get_current_stock(df: pd.DataFrame) -> pd.DataFrame:
    """Return the most recently recorded stock level for each item.

    The ``stock_remaining`` column in the source data reflects the stock
    *after* that day's sales have been deducted.  Therefore the latest
    date row for each item holds the current on-hand quantity.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.

    Returns
    -------
    pd.DataFrame
        Columns: item_name, category, current_stock.
    """

    # Sort ascending so that the last row per group is the most recent one.
    df_sorted = df.sort_values("date")

    # Keep the last (most recent) record per item.
    latest = (
        df_sorted
        .groupby("item_name", as_index=False)
        .last()  # last() after sort gives the latest-date row
        [["item_name", "category", "stock_remaining"]]
        .rename(columns={"stock_remaining": "current_stock"})
        .reset_index(drop=True)
    )

    return latest


# ---------------------------------------------------------------------------
# 4. Low-stock items
# ---------------------------------------------------------------------------

def get_low_stock_items(df: pd.DataFrame, min_threshold: int = 10) -> pd.DataFrame:
    """Filter to items whose current stock is below a minimum threshold.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.
    min_threshold : int, optional
        Units below which an item is considered low-stock. Default: 10.

    Returns
    -------
    pd.DataFrame
        Subset of ``get_current_stock()`` where current_stock < min_threshold,
        sorted by current_stock ascending (most urgent first).
    """

    stock_df = get_current_stock(df)

    low = (
        stock_df[stock_df["current_stock"] < min_threshold]
        .sort_values("current_stock", ascending=True)
        .reset_index(drop=True)
    )

    return low


# ---------------------------------------------------------------------------
# 5. Restock suggestions
# ---------------------------------------------------------------------------

def get_restock_suggestions(
    df: pd.DataFrame,
    min_threshold: int = 10,
    lead_days: int = 3,
) -> pd.DataFrame:
    """Generate restock quantity suggestions for under-stocked items.

    Formula
    -------
    avg_daily_sales       = total_units_sold_for_item / days_item_appeared
    buffer                = round(avg_daily_sales * lead_days)
    suggested_restock_qty = max(0, min_threshold + buffer - current_stock)

    Items with suggested_restock_qty == 0 are excluded from the result.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.
    min_threshold : int, optional
        Safety-stock floor. Default: 10.
    lead_days : int, optional
        Number of days of sales buffer to add on top of the threshold.
        Default: 3.

    Returns
    -------
    pd.DataFrame
        Columns: item_name, current_stock, avg_daily_sales,
                 suggested_restock_qty, calculation_note.
        Only rows where suggested_restock_qty > 0.
    """

    # --- Build the building blocks -----------------------------------------
    stock_df = get_current_stock(df)  # item_name, category, current_stock
    sales_df = get_product_sales(df)  # item_name, category, total_units_sold, total_revenue_inr

    # Count the number of distinct dates each item appears in the dataset.
    # We use this as the denominator for avg_daily_sales rather than the
    # total calendar length of the dataset, because an item not sold on a day
    # simply has no row in the CSV.
    days_per_item = (
        df.groupby("item_name")["date"]
        .nunique()
        .rename("days_in_data")
        .reset_index()
    )

    # --- Merge everything onto one frame ------------------------------------
    merged = (
        stock_df
        .merge(sales_df[["item_name", "total_units_sold"]], on="item_name", how="left")
        .merge(days_per_item, on="item_name", how="left")
    )

    # --- Compute avg_daily_sales --------------------------------------------
    # Guard against division by zero (shouldn't happen with clean data, but
    # defensive coding is worthwhile here).
    merged["avg_daily_sales"] = (
        merged["total_units_sold"] / merged["days_in_data"].replace(0, 1)
    ).round(2)

    # --- Compute restock quantity -------------------------------------------
    merged["buffer"] = (merged["avg_daily_sales"] * lead_days).round(0).astype(int)
    merged["suggested_restock_qty"] = (
        (min_threshold + merged["buffer"] - merged["current_stock"])
        .clip(lower=0)
        .astype(int)
    )

    # --- Build human-readable calculation notes ----------------------------
    def _make_note(row) -> str:
        return (
            f"Stock: {row['current_stock']} | "
            f"Threshold: {min_threshold} | "
            f"Buffer ({lead_days} days × {row['avg_daily_sales']}/day): {row['buffer']} | "
            f"Suggested: {row['suggested_restock_qty']}"
        )

    merged["calculation_note"] = merged.apply(_make_note, axis=1)

    # --- Filter and clean up ------------------------------------------------
    result = (
        merged[merged["suggested_restock_qty"] > 0]
        [["item_name", "current_stock", "avg_daily_sales",
          "suggested_restock_qty", "calculation_note"]]
        .sort_values("suggested_restock_qty", ascending=False)
        .reset_index(drop=True)
    )

    return result


# ---------------------------------------------------------------------------
# 6. Fast and slow movers
# ---------------------------------------------------------------------------

def get_fast_slow_movers(
    df: pd.DataFrame,
    top_n: int = 3,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Identify the top-N fast movers and bottom-N slow movers by units sold.

    Parameters
    ----------
    df : pd.DataFrame
        Clean DataFrame from ``load_data()``.
    top_n : int, optional
        Number of items to include in each list. Default: 3.

    Returns
    -------
    fast_movers : pd.DataFrame
        Top *top_n* items ranked by total_units_sold descending.
    slow_movers : pd.DataFrame
        Bottom *top_n* items ranked by total_units_sold ascending (fewest sold
        first), i.e. the slowest sellers.
    """

    sales = get_product_sales(df)  # already sorted by total_units_sold desc

    # Fast movers: highest unit sales → take the first top_n rows.
    fast_movers = sales.head(top_n).reset_index(drop=True)

    # Slow movers: lowest unit sales → take the last top_n rows, then sort
    # ascending so that the slowest item appears first.
    slow_movers = (
        sales.tail(top_n)
        .sort_values("total_units_sold", ascending=True)
        .reset_index(drop=True)
    )

    return fast_movers, slow_movers
