# Fieldwork Documentation
## Local Shop Stock & Sales Assistant

**Assignment:** 1-Day Take-Home Project — B.Tech
**Prepared by:** [Your Name]
**Date:** 13 November 2026

---

> ⚠️ **IMPORTANT DISCLOSURE — READ BEFORE SUBMISSION**
>
> This fieldwork document is based on a **hypothetical scenario** constructed from
> publicly available knowledge about how small kirana stores in India typically operate.
>
> **No real shopkeeper was interviewed. No real shop was visited.**
> No photographs were taken. No real sales data was collected.
>
> This scenario is used solely as a realistic basis for designing and prototyping a
> software solution. It is **not presented as real fieldwork.**
>
> If your evaluator requires real fieldwork, this document must be replaced with
> genuine interview notes, photographs, and data before submission.

---

## Scenario Description

| Field | Value |
|---|---|
| Shop type | Small kirana (general grocery) store |
| Shop name | *(hypothetical — not a real shop)* |
| Shopkeeper | *(hypothetical — not a real person)* |
| Role | Sole owner-operator |
| Location | Small town, Assam, India *(representative)* |
| Scenario basis | Common operational patterns of Indian kirana stores |

---

## Hypothetical Scenario Narrative

A small kirana store in a residential neighbourhood sells everyday grocery items:
rice, pulses, cooking oil, spices, biscuits, soap, shampoo sachets, and similar goods.

The shop is run by one person, typically open from 7 AM to 10 PM.
The owner has no formal accounting background and no digital tools.

### How stock and sales are currently managed (hypothetical)
- Every sale is written in a ruled notebook: item name, quantity, price.
- At the end of the day, the owner manually adds up totals — often taking 30–45 minutes.
- Stock levels are estimated from memory or by physically checking shelves.
- There is no system to flag when an item is about to run out.
- Ordering decisions are made based on intuition, sometimes resulting in overstocking
  slow-moving items or running out of fast-moving ones.

### Three representative pain points (hypothetical, not real quotes)
1. Daily revenue calculation is slow and error-prone when done by hand.
2. It is difficult to know which items need reordering without counting shelf stock manually.
3. There is no record of which items sell quickly and which sit unsold for weeks.

### One representative observation (hypothetical)
In a typical small kirana setup, the sales notebook is the single source of truth —
but it cannot be searched, sorted, or summarised without manual effort.

---

## What Real Fieldwork Would Require (Checklist)

If you replace this hypothetical document with real fieldwork, you must include:

- [ ] Shopkeeper's real name and consent to be named in the assignment
- [ ] Actual shop name and address
- [ ] Date and time of visit
- [ ] Method of data collection (notebook transcription, photographs, voice memo, etc.)
- [ ] At least two timestamped photographs of the shop or the existing record-keeping method
- [ ] Verbatim or paraphrased quotes from the shopkeeper
- [ ] At least 20 real transaction entries in `data/raw/stock_sales_raw.csv`
- [ ] Confirmation that the shopkeeper gave permission for their data to be used

---

## Data Collection Notes

Since no real data was collected, the file `data/raw/stock_sales_raw.csv` contains
**synthetic sample data** generated to represent the kinds of entries a small kirana
store might plausibly record.

This data is:
- Labelled clearly as synthetic in the CSV header comments
- Realistic in structure (item names, quantities, prices typical of Indian kirana stores)
- Not sourced from Kaggle, any external dataset, or any real shop

---

*Document version: 1.0 | Status: Hypothetical scenario — not real fieldwork*
