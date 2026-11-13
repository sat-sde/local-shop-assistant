# 🛒 Local Shop Stock & Sales Assistant

> **B.Tech 1-Day Take-Home Assignment — Python Application Development**
>
> ⚠️ **Disclosure:** This project is built on a **representative hypothetical scenario**
> for a small Indian kirana store. No real shopkeeper data is used.
> The scenario reflects common, well-documented challenges in Indian small retail.
> Replace `data/raw/stock_sales_raw.csv` with your own CSV file to analyse real data.

---

## 1. Problem Statement

Small kirana (general grocery) stores in India manage their stock and daily sales using
handwritten notebooks. This manual method makes it slow and error-prone to:

- Calculate total daily revenue without arithmetic mistakes
- Know which items are running low before they run out completely
- Identify which products sell quickly versus which sit unsold for weeks
- Decide how much of each item to reorder from the supplier

This application replaces the notebook with an interactive, data-driven dashboard
that reads a simple CSV file and delivers these answers instantly.

---

## 2. Real-World Motivation

India has over **12 million kirana stores** (Retailers Association of India).
The vast majority are run by one person or a family, with no digital tools.

The most common day-to-day problems these owners face:

| Problem | Impact |
|---|---|
| Manual addition at day's end | Takes 30–45 minutes; frequent errors |
| No stock visibility | Items run out unexpectedly; customers lost |
| No trend awareness | Overstocking slow items, understocking fast ones |
| Ordering by memory | Wrong quantities; waste or shortfall |

A lightweight Python tool that reads a CSV — something anyone can maintain in a
notebook then type up — directly addresses these problems without requiring internet
access, cloud accounts, or technical knowledge beyond basic computer use.

---

## 3. Who Benefits

| User | Benefit |
|---|---|
| **Shop owner** | Instant daily revenue total; no manual addition |
| **Shop owner** | Automatic low-stock alerts before items run out |
| **Shop owner** | Data-driven restock quantities instead of guesswork |
| **Family member helping in shop** | Clear visual charts, no training needed |
| **Student / developer** | Clean, readable Python codebase to learn from |

---

## 4. Features

### 📊 Dashboard
- Four headline metrics: Total Revenue, Units Sold, Products Tracked, Days Recorded
- Automatic low-stock alert table (items below configurable threshold)
- Data quality warning panel (shown only when CSV issues are detected)

### 📈 Sales Analysis
- Complete product-wise sales table sorted best-seller first
- Horizontal bar chart of revenue by product, colour-coded by category
- Side-by-side Top 3 Fast Sellers / Bottom 3 Slow Sellers

### 📦 Inventory Analysis
- Current stock table with low-stock rows highlighted in red
- Horizontal bar chart with configurable minimum-threshold line
- Clear note explaining how "current stock" is derived from the data

### 🔄 Restock Suggestions
- Calculated reorder quantities with full formula transparency
- Each suggestion shows: current stock, average daily sales, buffer days, suggested qty
- Expandable methodology explainer with formula and stated limitations
- Configurable minimum threshold and supplier lead days (sidebar)

### ⚙️ Data Validation (built into data loader)
- Detects missing values per column
- Flags quantity ≤ 0 or price ≤ 0 (rows kept, warning shown)
- Detects `total_inr` mismatches (tolerance ±₹1)
- Removes exact duplicate rows and reports count
- Raises clear errors for missing required columns or unreadable files
- Accepts both a file path (default CSV) and an uploaded file (Streamlit uploader)

---

## 5. Technologies Used

| Technology | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Primary language |
| Streamlit | 1.35+ | Web-based user interface |
| pandas | 2.0+ | CSV loading, data manipulation, analysis |
| Matplotlib | 3.8+ | Bar charts and stock level visualisations |
| Git | — | Version control |

No internet connection, cloud service, database, or external API is required.
The application runs entirely on a local machine.

---

## 6. Project Folder Structure

```
local-shop-assistant/
│
├── app.py                        ← Streamlit entry point (run this)
├── requirements.txt              ← Python dependencies
├── README.md                     ← This file
├── research.md                   ← Problem analysis, existing solutions, sources
├── fieldwork.md                  ← Scenario documentation
│
├── data/
│   └── raw/
│       └── stock_sales_raw.csv   ← Input data (replace with real data)
│
└── src/                          ← All application logic
    ├── __init__.py
    ├── data_loader.py            ← CSV loading and validation (10 checks)
    ├── analysis.py               ← All calculations (6 functions)
    └── components/               ← One file per UI tab
        ├── __init__.py
        ├── dashboard.py          ← Tab 1: Summary metrics + alerts
        ├── sales.py              ← Tab 2: Sales table + bar chart
        ├── inventory.py          ← Tab 3: Stock table + chart
        └── restock.py            ← Tab 4: Restock suggestions
```

**Separation of concerns:** `data_loader.py` handles input only. `analysis.py`
handles calculations only. Each component file handles display only. `app.py`
wires them together. This makes each file easy to read, test, and modify
independently.

---

## 7. Installation Instructions

### Prerequisites
- Python **3.10 or higher** installed on your system
- `pip` available (comes with Python)
- A terminal / command prompt

### Step 1 — Get the project
```bash
# If using Git:
git clone <your-repo-url>
cd local-shop-assistant

# Or simply download and unzip the project folder, then:
cd local-shop-assistant
```

### Step 2 — Create a virtual environment
```bash
# Mac / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

> The three packages installed are: `streamlit`, `pandas`, and `matplotlib`.

---

## 8. How to Run the Application

```bash
streamlit run app.py
```

Streamlit will print something like:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Open **http://localhost:8501** in any browser. The app loads immediately.

### Using your own data
1. Prepare a CSV file with these **exact column names**:

   | Column | Type | Example |
   |---|---|---|
   | `date` | YYYY-MM-DD | `2026-11-10` |
   | `item_name` | text | `Rice (1kg)` |
   | `category` | text | `Staples` |
   | `quantity_sold` | integer | `5` |
   | `price_per_unit_inr` | number | `52` |
   | `total_inr` | number | `260` |
   | `stock_remaining` | integer | `45` |

2. Either:
   - **Replace** `data/raw/stock_sales_raw.csv` with your file (keep the same name), or
   - **Upload** your file via the sidebar's "Upload your sales CSV" button

The app validates the file automatically and shows any issues found.

---

## 9. Actual Sample Output

The following output was generated by running the application against
`data/raw/stock_sales_raw.csv` (24 entries, 3 days, 11 products).

### Summary Metrics
```
Total Revenue   : ₹3,954.00
Total Units Sold: 101
Products Tracked: 11
Days Recorded   : 3  (2026-11-10 → 2026-11-12)
```

### Product Sales — Full Ranked Table
```
Product                   Category       Units Sold   Revenue (₹)
------------------------  -------------  ----------   -----------
Parle-G Biscuits          Snacks                 30           300
Rice (1kg)                Staples                15           780
Maggi Noodles (2-pack)    Snacks                 13           364
Toor Dal (500g)           Staples                10           650
Surf Excel (small)        Household               7           154
Sugar (1kg)               Staples                 6           264
Sunflower Oil (1L)        Staples                 6           810
Amul Butter (100g)        Dairy                   5           280
Lifebuoy Soap             Personal Care           5           160
Colgate Toothpaste (100g) Personal Care           3           162
Haldiram Namkeen          Snacks                  1            30
```

### Low Stock Alert (threshold: 10 units)
```
⚠️ 2 items are running low:

Product             Category   Stock Remaining
------------------  ---------  ---------------
Amul Butter (100g)  Dairy                    6   ← URGENT
Sunflower Oil (1L)  Staples                  6   ← URGENT
```

### Restock Suggestions (threshold: 10, lead time: 3 days)
```
Product                Current Stock   Avg Daily Sales   Suggested Order
---------------------  -------------   ---------------   ---------------
Amul Butter (100g)                 6              2.50                12
Sunflower Oil (1L)                 6              2.00                10
Toor Dal (500g)                   15              3.33                 5
Maggi Noodles (2-pack)            27              6.50                 3
Parle-G Biscuits                  38             10.00                 2
```

**Formula used:**
`Suggested Order = max(0, Threshold + round(Avg Daily Sales × Lead Days) − Current Stock)`

**Example for Amul Butter:**
`max(0, 10 + round(2.5 × 3) − 6)` = `max(0, 10 + 8 − 6)` = **12 units**

### Fast Movers vs Slow Movers
```
🏆 Top 3 Sellers          | 🐢 Bottom 3 Sellers
--------------------------|---------------------------
Parle-G Biscuits  — 30u   | Haldiram Namkeen   — 1u
Rice (1kg)        — 15u   | Colgate Toothpaste — 3u
Maggi Noodles     — 13u   | Lifebuoy Soap      — 5u
```

---

## 10. Screenshots

> 📷 **Screenshots are not included in this README.**
>
> To see the application in action, run it locally with `streamlit run app.py`
> and open http://localhost:8501 in your browser.
>
> A three-minute demonstration video is linked in Section 11 below.

---

## 11. Demonstration Video

> 🎥 **[Paste your video link here]**
>
> *Record a 3-minute screen recording of the running application covering:*
> *Dashboard → Sales Analysis → Inventory → Restock Suggestions → sidebar controls.*
> *Upload to YouTube (unlisted) or Google Drive (view link) and paste the URL above.*

---

## 12. Data Collection Methodology

> ⚠️ See [`fieldwork.md`](fieldwork.md) for the full scenario documentation.

The input data (`data/raw/stock_sales_raw.csv`) is **synthetic sample data** generated
to represent the kinds of daily sales entries a small kirana store might plausibly record.

**Structure of each data row:**
Each row represents one product sold on one day. It records:
- The date of sale
- The product name and category
- How many units were sold
- The price per unit and total amount
- How many units remained in stock after that day's sales

**To use real data:** Replace the CSV with actual records collected from a shop.
The column names must match exactly (see Section 8). The app will validate the
new file automatically on load.

---

## 13. Limitations

These are known, deliberate constraints — not bugs.

1. **Short data history inflates averages.**
   Restock suggestions are based on average daily sales. With only 3 days of data,
   one unusually busy or quiet day has a large effect on the average.
   The app warns about this in the Restock tab.

2. **Stock figures depend on accurate CSV entry.**
   The `stock_remaining` column must be manually updated each day. If sales happen
   without updating the file, the stock figures will be wrong.

3. **One entry per item per day assumed.**
   If the same item appears twice on the same day (two separate sales sessions),
   `get_current_stock()` uses the last row for that item on that day.
   The analysis module documents this in its `LIMITATIONS` docstring.

4. **No time-of-day tracking.**
   The CSV records daily totals. The app cannot show morning vs. evening patterns.

5. **Single-user, offline only.**
   Not suitable for a shop with multiple people entering data simultaneously.

6. **No export feature.**
   Results are displayed in the browser but cannot currently be saved to PDF or
   Excel directly from the UI.

7. **No GST, invoicing, or profit calculation.**
   Revenue shown is gross sales (qty × price). No cost-of-goods or profit margin
   analysis is included.

---

## 14. Future Improvements

| Improvement | Effort | Benefit |
|---|---|---|
| Export to CSV / PDF | Low | Shopkeeper can keep printed records |
| Multi-day trend chart | Medium | Shows whether sales are rising or falling |
| Profit margin column | Medium | Needs cost-price field added to CSV |
| Seasonal adjustment in restock | High | More accurate suggestions around festivals |
| Multi-user support | High | Multiple people can enter data |
| Mobile-friendly layout | Low | Better for use on a phone in the shop |
| Barcode-scan input | High | Faster data entry, fewer errors |

---

## 15. Git Commit History

```
9fb326a  Fix: load_data accepts file-like objects (Streamlit file upload support)
6543245  Fix: align app.py render calls to match component function names
f5bacfe  Add full Streamlit app: data_loader, analysis, components, app.py, README
8313a29  Initial commit: project structure, research.md, fieldwork.md, synthetic data
```

---

## Project Documents

| Document | Purpose |
|---|---|
| [`README.md`](README.md) | This file — full project documentation |
| [`research.md`](research.md) | Problem analysis, existing solutions, credible sources |
| [`fieldwork.md`](fieldwork.md) | Scenario documentation with full disclosure |
| [`data/raw/stock_sales_raw.csv`](data/raw/stock_sales_raw.csv) | Input data |

---

*Assignment: 1-Day Take-Home Project · B.Tech · November 2026*
*Language: Python 3 · UI: Streamlit · No external APIs or internet required*
