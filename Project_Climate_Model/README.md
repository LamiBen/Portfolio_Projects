# Predicting Daily Temperature from Location and Season

**Question:** How accurately can daily average temperature be predicted from a city's latitude, longitude, and time of year, for countries the model has never seen?

**Data:** City-level daily temperature records for 226 cities in 211 countries (82,391 city-days, September 2022 to September 2023), in `data/climate.csv`. Temperatures are never missing in this file.

**Method**
- **Features:** latitude, longitude, absolute latitude, the sine and cosine of the day of year, and interactions between latitude and the seasonal terms (seasons run in opposite directions in the two hemispheres).
- **Excluded on purpose:** the daily maximum and minimum temperatures, which are almost the target and would make the task trivial.
- **Evaluation:** 5-fold cross-validation grouped by country. Every test fold contains countries the model never saw in training, so neighbouring cities can't leak information into the test set.
- **Models:** a month-of-year average (the naive baseline), linear regression, and gradient boosting (scikit-learn `HistGradientBoostingRegressor`).

**Results (out-of-fold, every city-day predicted by a model that never saw its country)**

| Model | MAE (°C) | RMSE (°C) | R² |
|---|---|---|---|
| Month-of-year mean | 7.05 | 8.70 | 0.10 |
| Linear regression | 3.83 | 5.06 | 0.69 |
| Gradient boosting | **2.68** | **3.78** | **0.83** |

Gradient boosting is the most accurate of the three. Linear regression does much better than the naive baseline, which mixes hemispheres and so cannot capture the opposite seasons.

**Where the model struggles**
- **Hardest countries** (mean absolute error about 9 to 11°C): Colombia, Afghanistan, Bhutan, Ethiopia, and Mongolia. Several of these are highland or landlocked countries. Elevation is not in the dataset, so this is a hypothesis to test, not a finding.
- **Easiest countries** (mean absolute error of about 0.5°C or less): small countries such as the Marshall Islands, Liberia, and Benin, which have low seasonal swings (a standard deviation of 1.5°C or less across the year). Less variation leaves less to get wrong.

**Caveats**
- The data covers one year, so "seasonality" is learned from a single cycle.
- Most countries are represented by one city, so the test folds measure how well the model generalises across places, not across whole countries.

**Next steps**
- Add elevation data to test the highland explanation.
- Compare against a model that uses the country's climate zone, if you have one.

**Files**
- `climate_model.py`: feature engineering, country-grouped evaluation, and the figure (`python climate_model.py`, about 8 seconds)
- `figures/model_comparison.png`: MAE by model, and predicted against actual temperature for gradient boosting
- `data/climate.csv`: the source data (copied from the `weather_dash` repository)
