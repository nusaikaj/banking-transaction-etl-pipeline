import argparse
import logging
from pathlib import Path
from .extract import extract_data
from .transform import transform_data
from .load import load_data

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def run_pipeline(input_path, output_path, threshold=50000, skip_db=False, database_url=None):
    raw = extract_data(input_path)
    cleaned = transform_data(raw, suspicious_threshold=threshold)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output, index=False, date_format="%Y-%m-%d")
    logging.info("Extracted %s rows; cleaned %s rows; rejected/deduplicated %s rows", len(raw), len(cleaned), len(raw)-len(cleaned))
    if skip_db:
        logging.info("Database load skipped (--skip-db). CSV saved at %s", output)
    else:
        rows = load_data(cleaned, database_url=database_url)
        logging.info("Successfully loaded %s rows to database", rows)
    return len(cleaned)

def main():
    parser = argparse.ArgumentParser(description="Banking transaction CSV ETL")
    parser.add_argument("--input", type=Path, default=PROJECT_ROOT / "data" / "raw_transactions.csv")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "data" / "cleaned_transactions.csv")
    parser.add_argument("--threshold", type=float, default=50000)
    parser.add_argument("--skip-db", action="store_true", help="Validate and export without connecting to MySQL")
    parser.add_argument("--database-url", default=None, help="Override DB connection (avoid putting passwords in shell history)")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        run_pipeline(args.input, args.output, args.threshold, args.skip_db, args.database_url)
    except Exception:
        logging.exception("ETL failed. It did NOT complete successfully.")
        return 1
    logging.info("ETL pipeline completed successfully")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
