"""Movie recommender on MovieLens ratings.

Compares simple baselines with a biased matrix factorisation model trained
by stochastic gradient descent, evaluated on a held-out 20% of ratings.

Run from this folder:  python recommender.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path(__file__).resolve().parent.parent / "Project_Movies" / "data"
OUT = Path(__file__).resolve().parent / "figures"
SEED = 42
RELEVANT = 4.0  # a held-out rating >= 4 counts as "liked" for top-N precision
TOP_N = 10


def load_ratings():
    ratings = pd.read_csv(DATA / "ratings.csv")
    movies = pd.read_csv(DATA / "movies.csv")
    return ratings, movies


def split_per_user(ratings, test_frac=0.2, seed=SEED):
    """Hold out 20% of each user's ratings so every user appears in training."""
    rng = np.random.default_rng(seed)
    test_idx = []
    for _, group in ratings.groupby("userId"):
        n_test = max(1, int(round(len(group) * test_frac)))
        test_idx.extend(rng.choice(group.index.to_numpy(), n_test, replace=False))
    test = ratings.loc[test_idx]
    train = ratings.drop(index=test_idx)
    return train, test


def rmse(y, p):
    return float(np.sqrt(np.mean((y - p) ** 2)))


def mae(y, p):
    return float(np.mean(np.abs(y - p)))


def baseline_predictions(train, test):
    """Global mean, user mean and item mean, with fallbacks for unseen ids."""
    global_mean = train["rating"].mean()
    user_mean = train.groupby("userId")["rating"].mean()
    item_mean = train.groupby("movieId")["rating"].mean()

    p_global = np.full(len(test), global_mean)
    p_user = test["userId"].map(user_mean).fillna(global_mean).to_numpy()
    p_item = test["movieId"].map(item_mean).fillna(global_mean).to_numpy()
    return {"Global mean": p_global, "User mean": p_user, "Item mean": p_item}


class BiasedMF:
    """Rating ≈ mu + b_user + b_item + p_user · q_item, fitted with SGD."""

    def __init__(self, n_factors=20, lr=0.01, reg=0.05, epochs=25, seed=SEED):
        self.k, self.lr, self.reg, self.epochs, self.seed = n_factors, lr, reg, epochs, seed

    def fit(self, train):
        rng = np.random.default_rng(self.seed)
        self.user_ids = {u: i for i, u in enumerate(train["userId"].unique())}
        self.item_ids = {m: i for i, m in enumerate(train["movieId"].unique())}
        u = train["userId"].map(self.user_ids).to_numpy()
        i = train["movieId"].map(self.item_ids).to_numpy()
        r = train["rating"].to_numpy()

        self.mu = r.mean()
        self.bu = np.zeros(len(self.user_ids))
        self.bi = np.zeros(len(self.item_ids))
        self.P = rng.normal(0, 0.1, (len(self.user_ids), self.k))
        self.Q = rng.normal(0, 0.1, (len(self.item_ids), self.k))

        self.train_rmse = []
        order = np.arange(len(r))
        for _ in range(self.epochs):
            rng.shuffle(order)
            for idx in order:
                uu, ii = u[idx], i[idx]
                pu, qi = self.P[uu].copy(), self.Q[ii].copy()
                err = r[idx] - (self.mu + self.bu[uu] + self.bi[ii] + pu @ qi)
                self.bu[uu] += self.lr * (err - self.reg * self.bu[uu])
                self.bi[ii] += self.lr * (err - self.reg * self.bi[ii])
                self.P[uu] += self.lr * (err * qi - self.reg * pu)
                self.Q[ii] += self.lr * (err * pu - self.reg * qi)
            self.train_rmse.append(rmse(r, self.predict_pairs(train)))
        return self

    def predict_pairs(self, df):
        u = df["userId"].map(self.user_ids)
        i = df["movieId"].map(self.item_ids)
        known = u.notna() & i.notna()
        out = np.full(len(df), self.mu)
        uu = u[known].astype(int).to_numpy()
        ii = i[known].astype(int).to_numpy()
        out[known.to_numpy()] = (
            self.mu + self.bu[uu] + self.bi[ii] + np.sum(self.P[uu] * self.Q[ii], axis=1)
        )
        return np.clip(out, 0.5, 5.0)

    def scores_for_user(self, user_id):
        """Predicted rating for every movie this user has not already rated."""
        uu = self.user_ids[user_id]
        return self.mu + self.bu[uu] + self.bi + self.Q @ self.P[uu]


def top_n_precision(model, train, test, movies_index, n=TOP_N):
    """Share of recommended movies that the user liked in the held-out set."""
    liked = test[test["rating"] >= RELEVANT].groupby("userId")["movieId"].apply(set)
    seen = train.groupby("userId")["movieId"].apply(set)
    hits, total = 0, 0
    for user_id, liked_items in liked.items():
        if user_id not in model.user_ids:
            continue
        scores = model.scores_for_user(user_id)
        ids = np.array(list(model.item_ids.keys()))
        mask = ~np.isin(ids, list(seen.get(user_id, set())))
        candidates = ids[mask]
        top = candidates[np.argsort(-scores[mask])[:n]]
        hits += len(set(top) & liked_items)
        total += n
    return hits / total


def popularity_top_n_precision(train, test, n=TOP_N):
    """Baseline: recommend the most-rated movies the user has not seen."""
    counts = train["movieId"].value_counts()
    liked = test[test["rating"] >= RELEVANT].groupby("userId")["movieId"].apply(set)
    seen = train.groupby("userId")["movieId"].apply(set)
    hits, total = 0, 0
    for user_id, liked_items in liked.items():
        if user_id not in seen.index:
            continue
        top = [m for m in counts.index if m not in seen[user_id]][:n]
        hits += len(set(top) & liked_items)
        total += n
    return hits / total


def main():
    OUT.mkdir(exist_ok=True)
    ratings, movies = load_ratings()
    train, test = split_per_user(ratings)
    print(f"Train: {len(train):,} ratings | Test: {len(test):,} ratings")

    y = test["rating"].to_numpy()
    results = {}
    for name, pred in baseline_predictions(train, test).items():
        results[name] = {"RMSE": rmse(y, pred), "MAE": mae(y, pred)}

    model = BiasedMF().fit(train)
    pred = model.predict_pairs(test)
    results["Matrix factorisation"] = {"RMSE": rmse(y, pred), "MAE": mae(y, pred)}

    table = pd.DataFrame(results).T.round(3)
    print("\nRating prediction on held-out ratings")
    print(table.to_string())

    prec_mf = top_n_precision(model, train, test, movies)
    prec_pop = popularity_top_n_precision(train, test)
    print(f"\nTop-{TOP_N} precision (share of recommendations rated >= {RELEVANT} in test)")
    print(f"  Popularity baseline:      {prec_pop:.3f}")
    print(f"  Matrix factorisation:     {prec_mf:.3f}")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    table["RMSE"].plot.bar(ax=axes[0], color=["#999", "#999", "#999", "#2a6f97"])
    axes[0].set_title("Held-out RMSE (lower is better)")
    axes[0].set_ylabel("RMSE")
    axes[0].tick_params(axis="x", rotation=20)
    axes[1].plot(range(1, len(model.train_rmse) + 1), model.train_rmse, marker="o")
    axes[1].set_title("Training RMSE by epoch")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("RMSE")
    fig.tight_layout()
    fig.savefig(OUT / "model_comparison.png", dpi=120)
    print(f"\nSaved {OUT / 'model_comparison.png'}")


if __name__ == "__main__":
    main()
