import pandas as pd


def transform_data(df):
    if df is None:
        print("No data to transform.")
        return None

    df = df.drop_duplicates()

    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna(
        subset=["transaction_id", "customer_id", "transaction_date", "amount"]
    )

    df["merchant"] = df["merchant"].fillna("Unknown")
    df["category"] = df["category"].fillna("Unknown")
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["location"] = df["location"].fillna("Unknown")
    df["status"] = df["status"].fillna("Unknown")

    df["is_suspicious"] = df["amount"].apply(
        lambda x: "Yes" if x >= 50000 else "No"
    )

    df.to_csv("data/cleaned_transactions.csv", index=False)

    print("Data transformed successfully.")
    return df