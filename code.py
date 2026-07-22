import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Отримайте історичні ринкові дані для вибраного фінансового інструменту.
# Ці дані повинні включати основні показники,
# такі як ціна відкриття, ціна закриття, максимум, мінімум і обсяг торгів.
data = yf.download("AAPL", start="2025-01-01", end="2026-01-01")
print(data.head())



