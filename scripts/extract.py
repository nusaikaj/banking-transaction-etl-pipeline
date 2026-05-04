import pandas as pd


def extract_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Data extracted successfully.")
        return df
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return None
    except Exception as e:
        print(f"Extraction error: {e}")
        return None