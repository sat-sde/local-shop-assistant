"""
data_loader.py
==============
Loads and validates the shop CSV data file.

Public API
----------
load_data(filepath) -> (DataFrame, issues_list)
"""

import os
import pandas as pd

# Columns that must be present in the CSV for downstream analysis to work.
REQUIRED_COLUMNS = [
    "date",
    "item_name",
    "category",
    "quantity_sold",
    "price_per_unit_inr",
    "total_inr",
    "stock_remaining",
]


def load_data(filepath: str) -> tuple[pd.DataFrame, list[str]]:
    """Load and validate the stock/sales CSV file.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    df : pd.DataFrame
        Cleaned DataFrame ready for analysis.
    issues : list[str]
        Human-readable warning strings describing any data-quality problems
        found.  Empty list means the data is clean.

    Raises
    ------
    FileNotFoundError
        If *filepath* does not exist on disk.
    ValueError
        If the file is not parseable as CSV, or if one or more required
        columns are missing.
    """

    issues: list[str] = []

    # ------------------------------------------------------------------
    # 1. File-existence check
    # ------------------------------------------------------------------
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"CSV file not found: '{filepath}'. "
            "Please check the path and try again."
        )

    # ------------------------------------------------------------------
    # 2. Parse CSV
    # ------------------------------------------------------------------
    try:
        df = pd.read_csv(filepath)
    except Exception as exc:
        raise ValueError(
            f"Could not parse '{filepath}' as a CSV file. "
            f"Original error: {exc}"
        ) from exc

    # ------------------------------------------------------------------
    # 3. Required-column check — fail fast if the schema is wrong
    # ------------------------------------------------------------------
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"The following required columns are absent from '{filepath}': "
            f"{missing_cols}. "
            f"Found columns: {list(df.columns)}"
        )

    # ------------------------------------------------------------------
    # 4. Strip whitespace from string columns before any other checks
    #    so that "Rice " and "Rice" are treated as the same item.
    # ------------------------------------------------------------------
    for col in ("item_name", "category"):
        if df[col].dtype == object:
            df[col] = df[col].str.strip()

    # ------------------------------------------------------------------
    # 5. Drop fully duplicate rows and report
    # ------------------------------------------------------------------
    n_before = len(df)
    df = df.drop_duplicates()
    n_dropped = n_before - len(df)
    if n_dropped > 0:
        issues.append(
            f"Dropped {n_dropped} fully duplicate row(s) from the dataset."
        )

    # ------------------------------------------------------------------
    # 6. Parse dates; flag rows whose date cannot be parsed
    # ------------------------------------------------------------------
    # errors="coerce" turns unparseable values into NaT instead of raising.
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    bad_date_mask = df["date"].isna()
    if bad_date_mask.any():
        bad_indices = df.index[bad_date_mask].tolist()
        issues.append(
            f"{bad_date_mask.sum()} row(s) have unparseable dates "
            f"(row indices: {bad_indices}). Those rows have NaT in 'date'."
        )

    # ------------------------------------------------------------------
    # 7. Flag missing values per column
    # ------------------------------------------------------------------
    for col in REQUIRED_COLUMNS:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            issues.append(
                f"Column '{col}' has {n_missing} missing value(s)."
            )

    # ------------------------------------------------------------------
    # 8. Flag invalid quantity_sold (<= 0) — do NOT drop
    # ------------------------------------------------------------------
    invalid_qty_mask = df["quantity_sold"] <= 0
    if invalid_qty_mask.any():
        bad_indices = df.index[invalid_qty_mask].tolist()
        issues.append(
            f"{invalid_qty_mask.sum()} row(s) have quantity_sold <= 0 "
            f"(row indices: {bad_indices}). These rows are kept but may "
            "skew analysis results."
        )

    # ------------------------------------------------------------------
    # 9. Flag invalid price_per_unit_inr (<= 0) — do NOT drop
    # ------------------------------------------------------------------
    invalid_price_mask = df["price_per_unit_inr"] <= 0
    if invalid_price_mask.any():
        bad_indices = df.index[invalid_price_mask].tolist()
        issues.append(
            f"{invalid_price_mask.sum()} row(s) have price_per_unit_inr <= 0 "
            f"(row indices: {bad_indices}). These rows are kept but may "
            "skew revenue calculations."
        )

    # ------------------------------------------------------------------
    # 10. Flag total_inr mismatches (tolerance ±1 INR)
    #     Expected: total_inr ≈ quantity_sold × price_per_unit_inr
    # ------------------------------------------------------------------
    expected_total = df["quantity_sold"] * df["price_per_unit_inr"]
    mismatch_mask = (df["total_inr"] - expected_total).abs() > 1.0
    if mismatch_mask.any():
        bad_indices = df.index[mismatch_mask].tolist()
        issues.append(
            f"{mismatch_mask.sum()} row(s) have total_inr that does not match "
            f"quantity_sold × price_per_unit_inr (tolerance ±₹1) "
            f"(row indices: {bad_indices}). Consider verifying the source data."
        )

    return df, issues
