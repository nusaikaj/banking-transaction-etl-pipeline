import pandas as pd

OPTIONAL_COLUMNS = ("customer_name", "transaction_type", "merchant", "category", "payment_method", "location", "status")

def transform_data(df, suspicious_threshold=50000):
    if df is None or df.empty:
        raise ValueError("Cannot transform empty data")
    if suspicious_threshold < 0:
        raise ValueError("Threshold must not be negative")
    cleaned = df.copy()
    cleaned["transaction_id"] = cleaned["transaction_id"].astype("string").str.strip()
    cleaned["customer_id"] = cleaned["customer_id"].astype("string").str.strip()
    cleaned["transaction_date"] = pd.to_datetime(cleaned["transaction_date"], errors="coerce")
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    for col in OPTIONAL_COLUMNS:
        if col not in cleaned:
            cleaned[col] = "Unknown"
        cleaned[col] = cleaned[col].fillna("Unknown").astype("string").str.strip().replace("", "Unknown")
    required = ["transaction_id", "customer_id", "transaction_date", "amount"]
    cleaned = cleaned.dropna(subset=required)
    cleaned = cleaned.loc[(cleaned.transaction_id != "") & (cleaned.customer_id != "") & (cleaned.amount >= 0)].copy()
    # Keep last occurrence by business identifier so reruns are deterministic.
    cleaned = cleaned.drop_duplicates(subset=["transaction_id"], keep="last")
    if cleaned.empty:
        raise ValueError("No valid transactions after cleaning")
    cleaned["is_suspicious"] = cleaned["amount"].ge(suspicious_threshold).map({True: "Yes", False: "No"})
    return cleaned.reset_index(drop=True)
