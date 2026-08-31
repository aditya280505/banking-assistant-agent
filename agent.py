
import pandas as pd


# 1. Retrieve Transactions
def retrieve_transactions():
    try:
        df = pd.read_csv("data/transactions.csv")
        df["date"] = pd.to_datetime(df["date"])
        return df

    except Exception as e:
        raise Exception(f"Unable to retrieve transactions: {e}")


# 2. Filter Transactions
def filter_transactions(df, amount_limit=50000):
    today = pd.Timestamp.today()

    # Find previous month
    first_day_current = today.replace(day=1)
    last_day_previous = first_day_current - pd.Timedelta(days=1)
    first_day_previous = last_day_previous.replace(day=1)

    filtered = df[
        (df["date"] >= first_day_previous) &
        (df["date"] <= last_day_previous) &
        (df["amount"] > amount_limit) &
        (df["transaction_type"] == "Expense")
    ]

    return filtered


# 3. Categorize Transactions
def categorize_transactions(df):
    if df.empty:
        return pd.Series(dtype="float64")

    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


# 4. Calculate Total Spending
def calculate_total(df):
    return df["amount"].sum()


# 5. Detect Anomalies
def detect_anomalies(df):
    if df.empty:
        return pd.DataFrame()

    # Transactions significantly higher than average
    threshold = df["amount"].mean() * 1.5

    return df[df["amount"] > threshold]


# 6. Generate Spending Summary
def generate_summary(df, category_totals, total):

    if df.empty:
        return (
            "No transactions above ₹50,000 "
            "were found for last month."
        )

    highest_category = category_totals.index[0]
    highest_amount = category_totals.iloc[0]

    summary = f"""
You had {len(df)} transactions above ₹50,000 last month.

Total spending from these transactions:
₹{total:,.2f}

Your highest spending category was:
{highest_category}

Amount spent in this category:
₹{highest_amount:,.2f}

Please review the highlighted transactions
for unusual spending.
"""

    return summary

