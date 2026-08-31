import pandas as pd
from datetime import datetime

def retrieve_transactions():
    try:
        df = pd.read_csv("data/transactions.csv")
        df["date"] = pd.to_datetime(df["date"])
        return df
    except Exception as e:
        raise Exception(f"Unable to retrieve transactions: {e}")


def filter_transactions(df, amount_limit=50000):
    today = pd.Timestamp.today()

    # Previous month
    first_day_current = today.replace(day=1)
    last_day_previous = first_day_current - pd.Timedelta(days=1)
    first_day_previous = last_day_previous.replace(day=1)

    filtered = df[
        (df["date"] >= first_day_previous) &
        (df["date"] <= last_day_previous) &
        (df["amount"] > amount_limit) &
        (df["type"] == "Debit")
    ]

    return filtered


def categorize_transactions(df):
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)


def calculate_total(df):
    return df["amount"].sum()


def detect_anomalies(df):
    if df.empty:
        return pd.DataFrame()

    threshold = df["amount"].mean() * 1.5
    return df[df["amount"] > threshold]


def generate_summary(df, category_totals, total):
    if df.empty:
        return "No transactions above ₹50,000 were found for last month."

    highest_category = category_totals.index[0]

    summary = f"""
You had {len(df)} transactions above ₹50,000 last month.

Total spending from these transactions: ₹{total:,.2f}

Your highest spending category was {highest_category},
with ₹{category_totals.iloc[0]:,.2f} spent.

Please review the highlighted transactions for unusual spending.
"""

    return summary