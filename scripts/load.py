import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine


def load_data(df):
    if df is None:
        print("No data to load.")
        return

    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = quote_plus(os.getenv("DB_PASSWORD"))
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")

    try:
        engine = create_engine(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
        )

        df.to_sql(
            name="transactions",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Data loaded successfully into MySQL.")

    except Exception as e:
        print(f"Loading error: {e}")