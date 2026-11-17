"""How has the variety of US baby names changed since 1880?

Measures per year: number of distinct names, share of births in the top 100
names, Shannon entropy of the name distribution, and the share of births given
to 'unisex' names (names used for a substantial share of both sexes).

Run from this folder:  python name_diversity.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

NAMES_DIR = Path(__file__).resolve().parent.parent / "Project_Babynames" / "data" / "names"
OUT = Path(__file__).resolve().parent / "figures"
UNISEX_MIN_SHARE = 0.10  # a name is unisex if its less common sex is >= 10% of its births


def load_year(path):
    df = pd.read_csv(path, names=["name", "sex", "births"])
    df["year"] = int(path.stem.replace("yob", ""))
    return df


def yearly_metrics(df):
    rows = []
    for year, g in df.groupby("year"):
        total = g["births"].sum()
        by_name = g.groupby("name")["births"].sum()
        p = by_name / total
        top100_share = by_name.nlargest(100).sum() / total

        by_name_sex = g.pivot_table(index="name", columns="sex", values="births",
                                    aggfunc="sum", fill_value=0)
        name_total = by_name_sex.sum(axis=1)
        minor = by_name_sex.min(axis=1) / name_total
        unisex_births = name_total[minor >= UNISEX_MIN_SHARE].sum()

        rows.append({
            "year": year,
            "births": int(total),
            "distinct_names": int(by_name.size),
            "top100_share": round(top100_share, 4),
            "entropy_bits": round(float(-(p * np.log2(p)).sum()), 3),
            "unisex_share": round(unisex_births / total, 4),
        })
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(exist_ok=True)
    files = sorted(NAMES_DIR.glob("yob*.txt"))
    df = pd.concat([load_year(f) for f in files], ignore_index=True)
    metrics = yearly_metrics(df)

    csv_path = OUT / "yearly_name_diversity.csv"
    metrics.to_csv(csv_path, index=False)
    print(f"Years: {metrics['year'].min()}–{metrics['year'].max()} ({len(metrics)} years)")
    print(metrics.iloc[[0, 25, 50, 75, -1]].to_string(index=False))

    decades = metrics.set_index("year")
    print("\nChange from 1880 to 2022")
    for col in ["distinct_names", "top100_share", "entropy_bits", "unisex_share"]:
        start, end = decades.loc[1880, col], decades.loc[2022, col]
        print(f"  {col:15s} {start:>10} -> {end:>10}")

    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=True)
    panels = [
        ("distinct_names", "Distinct names per year"),
        ("top100_share", "Share of births in top 100 names"),
        ("entropy_bits", "Name entropy (bits)"),
        ("unisex_share", "Share of births to unisex names"),
    ]
    for ax, (col, title) in zip(axes.flat, panels):
        ax.plot(metrics["year"], metrics[col], color="#2a6f97")
        ax.set_title(title)
        ax.grid(alpha=0.3)
    for ax in axes[1]:
        ax.set_xlabel("Year")
    fig.tight_layout()
    fig.savefig(OUT / "name_diversity.png", dpi=120)
    print(f"\nSaved {OUT / 'name_diversity.png'} and {csv_path}")


if __name__ == "__main__":
    main()
