"""Generate reproducible, entirely fictional banking transactions for load testing."""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def generate(path, count=10000, seed=42):
    rng = random.Random(seed)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["transaction_id", "customer_id", "customer_name", "transaction_date", "amount", "transaction_type", "merchant", "category", "payment_method", "location", "status"]
    categories = [("Groceries", "Sample Grocery"), ("Transport", "Sample Transport"), ("Bills", "Sample Utility"), ("Shopping", "Sample Store"), ("Income", "Sample Employer")]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields)
        writer.writeheader()
        for i in range(1, count + 1):
            category, merchant=rng.choice(categories)
            writer.writerow({"transaction_id":f"SYN{i:07d}", "customer_id":f"SYN-C{rng.randint(1,500):04d}", "customer_name":"Fictional Customer", "transaction_date":(date(2026,1,1)+timedelta(days=rng.randrange(180))).isoformat(), "amount":round(rng.uniform(100,100000),2), "transaction_type": "Credit" if category=="Income" else "Debit", "merchant":merchant, "category":category, "payment_method":rng.choice(["Card","Online","Bank Transfer"]), "location":rng.choice(["Colombo","Kandy","Galle","Jaffna"]), "status":rng.choices(["Success","Failed"],weights=[95,5])[0]})
    return path

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--rows',type=int,default=10000)
    ap.add_argument('--output',type=Path,default=ROOT/'data'/'synthetic_transactions.csv')
    args=ap.parse_args()
    if args.rows < 1: ap.error('--rows must be positive')
    print(f"Generated {args.rows:,} synthetic records: {generate(args.output,args.rows)}")
