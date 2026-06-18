"""
Transform raw prices into a PAMI temporal transactional database.

Each trading day becomes a transaction containing discretized movement
labels (e.g. "SPY_up", "TLT_big_down"). PFPGrowth mines these for
cross-asset patterns that recur with bounded periodicity.

Usage: python build_temporal_db.py
Output: market_temporal_db.txt, daily_returns.csv
"""

import pandas as pd

prices = pd.read_csv("../data/raw_prices.csv", index_col=0)
returns = prices.pct_change().dropna() * 100

# Thresholds chosen to separate noise (±0.3%) from directional moves,
# with ±1.5% marking outsized days. Tune if pattern counts are too
# high (widen bins) or too low (narrow them).
bins = [-float("inf"), -1.5, -0.3, 0.3, 1.5, float("inf")]
labels = ["big_down", "down", "flat", "up", "big_up"]

# Keep returns intact for later signal testing; label a copy
labeled = returns.copy()
for ticker in labeled.columns:
    labeled[ticker] = ticker + "_" + pd.cut(returns[ticker], bins=bins, labels=labels).astype(str)

print("SPY label distribution:")
print(labeled["SPY"].str.replace("SPY_", "").value_counts().sort_index())

returns.to_csv("../data/daily_returns.csv")

# PAMI temporal DB format: integer timestamp, then tab-separated items
with open("../data/market_temporal_db.txt", "w") as f:
    for i, row in enumerate(labeled.values, start=1):
        f.write(str(i) + "\t" + "\t".join(row) + "\n")

print(f"Wrote {i} transactions to market_temporal_db.txt")