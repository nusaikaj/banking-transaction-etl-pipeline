import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from dotenv import load_dotenv


def load_data(df, database_url=None, table_name="transactions"):
    """Load a snapshot atomically by replacing rows inside a transaction.

    Snapshot mode is deliberate: rerunning the same CSV does not create duplicates.
    The table must be used exclusively by this pipeline during a refresh.
    """
    if df is None or df.empty:
        raise ValueError("Refusing to load empty data")
    load_dotenv()
    if database_url:
        engine = create_engine(database_url)
    elif os.getenv("DATABASE_URL"):
        engine = create_engine(os.environ["DATABASE_URL"])
    else:
        required = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME")
        missing = [key for key in required if os.getenv(key) is None]
        if missing:
            raise ValueError("Database configuration missing: " + ", ".join(missing))
        engine = create_engine(URL.create(
            "mysql+pymysql", username=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"], host=os.environ["DB_HOST"],
            port=int(os.getenv("DB_PORT", "3306")), database=os.environ["DB_NAME"]
        ))
    # In transactional databases, data deletion + insertion are committed together.
    # For a first run, to_sql creates the table; subsequent runs refresh its rows.
    try:
        with engine.begin() as conn:
            inspector = __import__('sqlalchemy').inspect(conn)
            if inspector.has_table(table_name):
                if not table_name.replace('_', '').isalnum():
                    raise ValueError("Invalid table name")
                conn.execute(text(f"DELETE FROM `{table_name}`" if conn.dialect.name == 'mysql' else f'DELETE FROM "{table_name}"'))
            df.to_sql(table_name, con=conn, if_exists="append", index=False, method="multi", chunksize=1000)
    finally:
        engine.dispose()
    return len(df)
