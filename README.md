# Local Shop Stock & Sales Assistant

> ℹ️ **Disclosure:** This application uses synthetic sample data representative of a small Indian kirana store. No real shopkeeper data is used. Replace `data/raw/stock_sales_raw.csv` with your own CSV to analyse real data.

---

## What This App Does

The Local Shop Stock & Sales Assistant is a lightweight Streamlit dashboard built to help small kirana store owners make sense of their daily sales data — without needing a spreadsheet or accounting background.

The app is organised into four tabs:

- **📊 Dashboard** — At-a-glance KPIs: total revenue, units sold, number of products tracked, and date range of the data. Fast-mover and slow-mover highlights give an instant feel for which items drive the business.
- **📈 Sales Analysis** — A deeper look at product-level performance: bar charts of revenue and units sold per item, category breakdowns, and a day-by-day sales trend over the data period.
- **📦 Inventory** — Current stock levels for every tracked item, with colour-coded low-stock alerts based on the threshold you configure in the sidebar.
- **🔄 Restock Suggestions** — Data-driven reorder recommendations that factor in your minimum stock threshold, average daily sales rate, and supplier lead time, with a plain-language explanation for every suggested quantity.

---

## Project Structure

```
local-shop-assistant/
├── app.py
├── requirements.txt
├── README.md
├── research.md
├── fieldwork.md
├── data/
│   ├── raw/
│   │   └── stock_sales_raw.csv
│   └── processed/   (created when app exports)
└── src/
    ├── data_loader.py
    ├── analysis.py
    └── components/
        ├── dashboard.py
        ├── sales.py
        ├── inventory.py
        └── restock.py
```

---

## How to Run Locally

### Prerequisites

- Python **3.10 or higher**
- `pip` (comes with Python)

### Steps

1. **Clone or download** the project folder to your machine.

2. **Open a terminal** and navigate into the project directory:
   ```bash
   cd local-shop-assistant
   ```

3. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Mac/Linux
   venv\Scripts\activate       # Windows
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the app:**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** and go to: [http://localhost:8501](http://localhost:8501)

> The app opens automatically in most setups. If it doesn't, copy the URL from the terminal output.

---

## Using Your Own Data

You have two options for loading your own sales data:

### Option A — Replace the default CSV

Overwrite the file at `data/raw/stock_sales_raw.csv` with your own CSV. The app loads this file automatically on startup.

### Option B — Upload via the sidebar

Use the **"Upload your sales CSV"** file uploader in the left sidebar. The uploaded file takes priority over the default CSV for that session.

### Required columns

Your CSV **must** contain the following columns (exact names, case-sensitive):

| Column | Description |
|---|---|
| `date` | Date of the sale (e.g. `2026-11-10`) |
| `item_name` | Name of the product |
| `category` | Product category (e.g. Staples, Dairy) |
| `quantity_sold` | Number of units sold on that date |
| `price_per_unit_inr` | Selling price per unit in Indian Rupees |
| `total_inr` | Total revenue for that row (`quantity_sold × price_per_unit_inr`) |
| `stock_remaining` | Stock left after that day's sales |

Additional columns are ignored. The app will show a warning for any data quality issues it detects (duplicate rows, mismatched totals, missing values, etc.).

---

## Limitations

1. **Small date range.** Restock suggestions are calculated from average daily sales across the available data. With only a few days of data the averages may not reflect true demand patterns — especially around festivals, weekends, or seasons.

2. **No forecasting.** The app does not predict future demand. It extrapolates from historical averages, which works well for stable, slow-changing products but poorly for seasonal or trending items.

3. **Single-location, single-supplier model.** The app assumes one store and one supplier lead time for all items. It does not handle multiple suppliers, locations, or partial deliveries.

4. **No write-back or persistent storage.** The app is read-only: it does not update stock levels, record new sales, or save user changes between sessions. It is an analysis and planning tool, not an inventory management system.

---

## Assignment Context

This prototype was built as a **1-day B.Tech take-home assignment**. The scenario — a small Indian kirana store analysing its stock and sales — is entirely hypothetical. The data is synthetic and was generated solely for demonstration purposes. The app is intended to illustrate applied data analysis and dashboard design skills, not to serve as a production system.
