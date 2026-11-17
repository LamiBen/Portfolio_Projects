# Müsli Orders: Shipping Mode Analysis

**Question:** Do different shipping modes differ in order quantity, discounts, and profit?

**Data:** Order-level records from an online retailer, with campaign data, order-process timestamps, and an internal intern dataset. Cleaned into `data/muesli_orders_clean.csv`.

**Method**
- Cleaned column names, checked for missing values, and parsed order dates.
- Extracted month, weekday, and other date features.
- Plotted order volume over short windows (one week, one month) and by weekday.
- Compared shipping modes with two-sample t-tests and a one-way ANOVA.

**Findings**
- **Quantity:** The t-test shows a statistically significant difference in average quantity between First Class and Standard Class shipping.
- **Discounts:** No statistically significant difference between First Class and Standard Class.
- **Profit:** No statistically significant difference in mean profit between First Class and Standard Class.
- **Profit across all modes:** The ANOVA finds no statistically significant difference in mean profit across shipping modes.

**Files**
- `project/Project.ipynb`: the analysis notebook
- `data/`: raw and cleaned order, campaign, and process data

**Note:** This project began as a Spiced Bootcamp coursework assignment. The statistical tests, interpretations, and cleaning steps shown here are my own.
