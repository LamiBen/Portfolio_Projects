"""Predict daily average temperature from location and season.

Evaluation uses GroupKFold on country, so every test fold contains countries
the model has never seen. A random split would let neighbouring cities from
the same country leak into training and overstate accuracy.

Features deliberately exclude avg_max_temp and avg_min_temp, which are almost
the target and would make the task trivial.

Run from this folder:  python climate_model.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
DATA = HERE / "data" / "climate.csv"
OUT = HERE / "figures"
N_FOLDS = 5


def build_features(df):
    doy = pd.to_datetime(df["date"]).dt.dayofyear.to_numpy()
    angle = 2 * np.pi * doy / 365.25
    sin_s, cos_s = np.sin(angle), np.cos(angle)
    lat = df["lat"].to_numpy()
    X = pd.DataFrame({
        "lat": lat,
        "lon": df["lon"].to_numpy(),
        "abs_lat": np.abs(lat),
        "sin_doy": sin_s,
        "cos_doy": cos_s,
        # Seasons run in opposite directions in the two hemispheres, so the
        # seasonal terms are interacted with latitude.
        "lat_x_sin": lat * sin_s,
        "lat_x_cos": lat * cos_s,
    })
    return X


def month_mean_baseline(train, test):
    """Predict each calendar month's average across the training data."""
    m_train = pd.to_datetime(train["date"]).dt.month
    m_test = pd.to_datetime(test["date"]).dt.month
    means = train.groupby(m_train)["avg_temp"].mean()
    return m_test.map(means).fillna(train["avg_temp"].mean()).to_numpy()


def evaluate(name, pred, y):
    return {
        "Model": name,
        "MAE (°C)": mean_absolute_error(y, pred),
        "RMSE (°C)": root_mean_squared_error(y, pred),
        "R²": r2_score(y, pred),
    }


def main():
    OUT.mkdir(exist_ok=True)
    df = pd.read_csv(DATA)
    df = df.dropna(subset=["avg_temp"]).reset_index(drop=True)
    X = build_features(df)
    y = df["avg_temp"].to_numpy()
    groups = df["country"].to_numpy()
    print(f"{len(df):,} city-days, {df['country'].nunique()} countries, {N_FOLDS}-fold CV by country")

    models = {
        "Month-of-year mean": None,
        "Linear regression": make_pipeline(StandardScaler(), LinearRegression()),
        "Gradient boosting": HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05,
                                                           random_state=0),
    }

    all_preds = {name: np.full(len(y), np.nan) for name in models}
    gkf = GroupKFold(n_splits=N_FOLDS)
    for train_idx, test_idx in gkf.split(X, y, groups):
        train, test = df.iloc[train_idx], df.iloc[test_idx]
        all_preds["Month-of-year mean"][test_idx] = month_mean_baseline(train, test)
        for name, model in models.items():
            if model is None:
                continue
            model.fit(X.iloc[train_idx], y[train_idx])
            all_preds[name][test_idx] = model.predict(X.iloc[test_idx])

    rows = [evaluate(name, all_preds[name], y) for name in models]
    results = pd.DataFrame(rows).set_index("Model").round(2)
    print("\nOut-of-fold results (every city-day predicted by a model that never saw its country)")
    print(results.to_string())

    # Where does the best model go wrong? Error by country, largest first.
    best = all_preds["Gradient boosting"]
    by_country = (df.assign(abs_err=np.abs(y - best))
                    .groupby("country")["abs_err"].mean()
                    .sort_values(ascending=False))
    print("\nHardest countries (mean absolute error, gradient boosting)")
    print(by_country.head(5).round(2).to_string())
    print("\nEasiest countries")
    print(by_country.tail(5).round(2).to_string())

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    results["MAE (°C)"].plot.bar(ax=axes[0], color=["#999", "#999", "#2a6f97"])
    axes[0].set_title("Out-of-country MAE (lower is better)")
    axes[0].set_ylabel("°C")
    axes[0].tick_params(axis="x", rotation=15)
    axes[1].scatter(y, best, s=3, alpha=0.2, color="#2a6f97")
    lims = [y.min(), y.max()]
    axes[1].plot(lims, lims, color="black", lw=1)
    axes[1].set_title("Gradient boosting: predicted vs actual")
    axes[1].set_xlabel("Actual average temperature (°C)")
    axes[1].set_ylabel("Predicted (°C)")
    fig.tight_layout()
    fig.savefig(OUT / "model_comparison.png", dpi=120)
    print(f"\nSaved {OUT / 'model_comparison.png'}")


if __name__ == "__main__":
    main()
