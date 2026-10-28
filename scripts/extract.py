from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"transaction_id", "customer_id", "transaction_date", "amount"}

def extract_data(file_path):
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {path}")
    df = pd.read_csv(path, dtype={"transaction_id": "string", "customer_id": "string"})
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required CSV columns: {', '.join(sorted(missing))}")
    if df.empty:
        raise ValueError("Input CSV contains no transactions")
    return df
