import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Отримайте історичні ринкові дані для вибраного фінансового інструменту.
# Ці дані повинні включати основні показники,
# такі як ціна відкриття, ціна закриття, максимум, мінімум і обсяг торгів.
data = yf.download("AAPL", start="2025-01-01", end="2026-01-01")
data.columns = data.columns.get_level_values(0)
# оскільки yfinance надає дані у MultiIndex,
# тому цим рядком ми отримаємо строку з назвами колонок(сlose, high, low і тд)

# 2. Організуйте отримані дані в структурований формат, наприклад DataFrame,
# гарантуючи, що вони чисті та готові для аналізу.
print(data.head())
# перевірка перших 5 рядків
print(data.info())
# інформація про DataFrame (стовпці, типи даних, кількість записів)
data = data.dropna()
# видалення пропущених значень (якщо вони є)
print(data.describe())
# основна статистика по числових даних

# 3. Розробіть базову модель торгівлі
data["SMA_short"] = data["Close"].rolling(window=20).mean()
data["SMA_long"] = data["Close"].rolling(window=50).mean()
# попередні 2 рядки рахують ковзні середні(moving average) для ціни закриття
# на періодах 20 та 50 днів відповідно
data = data.dropna()
# видалення пропущених якщо вони є
data["Signal"] = (data["SMA_short"] > data["SMA_long"]).astype(int)
# створення сигналів для кожного дня
# якщо True - 1, False - 0
data["Position"] = data["Signal"].diff()
# розрахунок моментів зміни сигналу

# 4. генерація торгових сигналів
data["Trade Signal"] = "Hold"
# за замувчуванням для всіх днів сигнал буде hold
data.loc[data["Position"] == 1, "Trade Signal"] = "Buy"
# якщо відбулося перетинання ковзних середніх вгору - Buy
# 1 змінюється на 0, типу 1-0=1
data.loc[data["Position"] == -1, "Trade Signal"] = "Sell"
# якщо відбулося перетинання ковзних середніх вниз - Sell
# 0-1=-1
print(data[["Close", "SMA_short", "SMA_long", "Signal", "Position", "Trade Signal"]].head(60))

# 5. Розрахунок прибутку та візуалізація
data["Return"] = data["Close"].pct_change()
# відсоткова зміна ціни закриття
data["Return_on_strategy"] = data["Return"] * data["Signal"].shift(1)
# дохідність за кожень день
data["Cumulative_Strategy"] = (1 + data["Return_on_strategy"]).cumprod()
# накопичена дохідність з початку періоду
