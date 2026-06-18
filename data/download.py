"""
Download daily close prices for a cross-asset ticker basket.
Covers equities, bonds, gold, and emerging markets to capture
diverse regime behaviors — single-asset-class data produces
trivial patterns.

Usage: python download.py
Output: raw_prices.csv
"""

import yfinance as yf
import pandas as pd

# Cross-asset basket: sectors + bonds + gold + EM for regime diversity
TICKERS = ["SPY", "QQQ", "IWM", "XLF", "XLE", "XLK", "XLV", "XLU", "GLD", "TLT", "EEM", "HYG"]

print(f"Downloading {len(TICKERS)} tickers...")
df = yf.download(TICKERS, start="2010-01-01", end="2025-12-31")["Close"]

# Forward-fill gaps from mismatched trading calendars (e.g. bond holidays)
df = df.ffill().dropna()

df.to_csv("raw_prices.csv")
print(f"Saved: {df.shape[0]} days x {df.shape[1]} tickers")
print(f"Date range: {df.index.min().date()} to {df.index.max().date()}")