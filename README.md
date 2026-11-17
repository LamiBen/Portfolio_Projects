# Lamiae Benouahi: Data Science & Analytics Portfolio

Data scientist and analyst based in Berlin. I work with Python, R, SQL, and BI tools (Power BI, Tableau, Looker Studio) to turn messy data into clear answers. This repository collects my exploratory analysis, statistical testing, and predictive modelling projects.

## Projects

| Project | Focus | Key skills |
|---|---|---|
| [Müsli orders](Project_Müsli/) | Shipping-mode analysis on an online retailer's orders: statistical tests on quantity, discounts, and profit | pandas, hypothesis testing (t-test, ANOVA), time-series plots |
| [Life expectancy vs fertility](Project_Gif(countries)/) | Cross-country analysis of life expectancy against fertility rate, with animated plots across decades | pandas, data merging, matplotlib, animated visualisation |
| [Car prices](Project_Cars/) | Predicting car prices from specifications, including cleaning, splitting, and model evaluation | pandas, scikit-learn, linear regression, MAE / MSE / R² |
| [Baby names](Project_Babynames/) | Name-frequency trends across US birth records from 1880 onwards | pandas, data parsing, aggregation |
| [MovieLens SQL](Project_Movies/) | 17 SQL queries on a movie ratings database, from simple filters to joins and aggregations | SQL, joins, aggregations |
| [Movie recommender](Project_Movie_Recommender/) | Matrix factorisation built from scratch vs baselines: better rating prediction, weaker top-10 ranking than popularity | NumPy, SGD, offline evaluation, model comparison |
| [Baby name diversity](Project_Name_Diversity/) | US naming trends, 1880–2022: a falling top-100 share and rising unisex naming, with fewer distinct names since 2008 | pandas, entropy, time-series analysis |
| [Temperature model](Project_Climate_Model/) | Predicting daily temperature for countries the model has never seen, with country-grouped cross-validation | scikit-learn, gradient boosting, leakage-aware evaluation |

Live dashboard: [Weather analysis of Africa's top diving destinations](https://weather-dashapp-qpu9.onrender.com) (source in the `weather_dash` repository).

## Notes on provenance

Some of these projects were completed as coursework during the Spiced Bootcamp Data Science programme. Where that applies, each project's README says so and describes my own analysis and changes.

## Running the notebooks

Each notebook reads its data with paths relative to its own folder, so they run from a fresh clone. Install the Python packages you need (`pandas`, `matplotlib`, `scikit-learn`, `imageio`, `openpyxl`, `xlrd`) and open the notebook in Jupyter.
