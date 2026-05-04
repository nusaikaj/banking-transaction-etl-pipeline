from extract import extract_data
from transform import transform_data
from load import load_data


def run_pipeline():
    raw_file_path = "data/raw_transactions.csv"

    print("Starting Banking Transaction ETL Pipeline...")

    raw_data = extract_data(raw_file_path)
    cleaned_data = transform_data(raw_data)
    load_data(cleaned_data)

    print("ETL Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()