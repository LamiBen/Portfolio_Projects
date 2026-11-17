# Car Price Prediction

**Question:** How well can a car's price be predicted from its specifications?

**Data:** A car listings dataset with make, model, year, engine details, horsepower, and MSRP. Cleaned copies are in `data/`.

**Method**
- Explored the data with `describe()`, price range, and make counts.
- Checked column names and removed duplicate rows.
- Dropped rows with missing values.
- Split features from the target (`price`), then into train, validation, and test sets.
- One-hot encoded categorical variables.
- Trained a linear regression model and evaluated it with MAE, MSE, and R².

**Files**
- `project/Project_Cars.ipynb`: the main analysis notebook
- `project/Project Cars.ipynb`: an earlier version of the same analysis
- `data/`: raw and cleaned datasets, plus a scratch notebook for cleaning

**Note:** This project began as a Spiced Bootcamp coursework assignment. The cleaning steps, feature preparation, and model evaluation are my own work.

**Possible next steps:** Try tree-based models and compare them against the linear baseline on the same validation split.
