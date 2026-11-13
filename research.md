# Research Document
## Local Shop Stock & Sales Assistant

**Assignment:** 1-Day Take-Home Project — B.Tech
**Date:** 13 November 2026
**Author:** [Your Name]

---

> ⚠️ **Disclosure**
> This project is based on a **representative hypothetical scenario** for a small Indian kirana (general) store.
> No real shopkeeper was interviewed. The scenario reflects common, well-documented challenges faced by
> small retailers in India and is used solely as a basis for building a software prototype.
> All details marked with 🔲 require real-world verification before any claim of fieldwork can be made.

---

## 1. Problem Identification

### Context
Small kirana stores are the backbone of retail in India. According to the Retailers Association of India,
there are over 12 million kirana stores operating across the country. The majority are run by a single
owner or family, with little to no use of digital tools.

### Identified Problem
**Difficulty tracking daily product sales and current stock levels using only handwritten records.**

A typical small kirana store owner:
- Writes each sale manually in a notebook or on loose paper.
- Has no quick way to know the current quantity of any item in stock.
- Cannot easily calculate daily revenue or profit without spending significant time at the end of the day.
- Cannot identify which items sell quickly (fast-moving) versus which sit unsold (slow-moving).

### Why This Problem Is Suitable for a 1-Day Assignment
- It is a **single, well-defined pain point** — not vague.
- It requires only a **CSV file and Python** to address meaningfully.
- The solution can be built, tested, and demonstrated within 4 hours of coding.
- It has real, measurable impact for the shop owner.

---

## 2. Why Solving This Helps the Shop Owner

| Pain Point | Impact of the Problem | How the App Helps |
|---|---|---|
| Manual addition errors | Wrong daily totals, financial loss | Auto-calculates totals |
| No stock visibility | Items run out unexpectedly | Shows low-stock alerts |
| No sales trends | Overstocks slow items, understocks fast ones | Shows fast/slow movers |
| Time spent on end-of-day accounting | Exhausting, error-prone | Generates instant daily summary |

---

## 3. Proposed Software Solution

A **command-line Python application** that:
1. Accepts product name, quantity sold, and price per unit as input.
2. Records each transaction to a CSV file.
3. Updates a running stock level.
4. Displays a daily sales summary (total revenue, units sold per item).
5. Flags items whose stock falls below a defined threshold.
6. Shows the top 3 fast-moving and bottom 3 slow-moving items.

**No internet, no cloud, no database required.** Runs entirely on the shopkeeper's computer or laptop.

---

## 4. Existing Solutions and Their Limitations

### Solution 1: Vyapar App (vyaparapp.in)
Vyapar is a popular Indian GST billing and inventory management app for small businesses.

**Why it may not fit this shopkeeper:**
- Requires a smartphone with reasonable storage and a stable internet connection for sync.
- The free tier has significant feature restrictions; full features require a paid subscription.
- It is designed around GST invoicing, which may be more complex than a small kirana owner needs.
- Has a learning curve that can be a barrier for owners with limited digital literacy.
- 🔲 *[Verify: Does the shopkeeper own a smartphone? Are they comfortable with app-based tools?]*

### Solution 2: Microsoft Excel / Google Sheets
Spreadsheets are commonly suggested as a step up from paper notebooks.

**Why it may not fit this shopkeeper:**
- Requires the user to design their own structure — no guided input.
- Easy to accidentally overwrite or delete data.
- Requires either a laptop with Excel or a Gmail account with consistent internet for Sheets.
- No automatic low-stock alerts without learning formulas or scripts.
- 🔲 *[Verify: Does the shopkeeper have a computer or reliable internet access?]*

---

## 5. Credible Sources for Research

1. **Retailers Association of India — State of Retail Report**
   - URL: https://www.rai.net.in
   - Relevance: Provides data on kirana store count, digitisation challenges, and retail trends in India.
   - Use: Cite for the scale of the problem (12M+ kirana stores).

2. **NASSCOM — SMB Digital Adoption Report**
   - URL: https://nasscom.in
   - Relevance: Documents barriers to digital tool adoption among small Indian businesses,
     including cost, language, and digital literacy.
   - Use: Cite for why existing solutions like Vyapar or Excel may not be adopted.

> 📌 **Note:** These are credible, publicly available Indian industry sources.
> You should visit these websites and locate the specific report or page to cite accurately.
> Do not cite them without reading the actual source.

---

## 6. Scope Boundary

This project will **not** include:
- GST calculation or invoicing
- Multi-user access
- Cloud storage or synchronisation
- Barcode scanning
- Profit/loss accounting (beyond simple revenue totals)

These are deliberate exclusions to keep the project achievable within one day.

---

*Document version: 1.0 | Status: Draft*
