import tempfile
import unittest
from pathlib import Path
import pandas as pd
from scripts.extract import extract_data
from scripts.transform import transform_data
from scripts.main import run_pipeline

class TestETL(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"transaction_id": ["A", "A", "B", "C", "D"], "customer_id": ["1", "1", "2", "3", "4"], "transaction_date": ["2026-01-01", "2026-01-01", "bad", "2026-01-02", "2026-01-03"], "amount": [100, 200, 300, -50, 50000]})
    def test_deduplication_invalid_rows_and_threshold(self):
        res=transform_data(self.df)
        self.assertEqual(len(res),2)
        self.assertEqual(res.loc[res.transaction_id == "A", "amount"].iloc[0],200)
        self.assertEqual(res.loc[res.transaction_id == "D", "is_suspicious"].iloc[0],"Yes")
    def test_no_input_mutation(self):
        transform_data(self.df)
        self.assertNotIn("is_suspicious", self.df.columns)
    def test_missing_required_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            f=Path(tmp)/"input.csv"
            pd.DataFrame({"wrong": [1]}).to_csv(f,index=False)
            with self.assertRaises(ValueError): extract_data(f)
    def test_csv_only_pipeline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp); raw=path/'raw.csv'; out=path/'clean.csv'
            self.df.to_csv(raw,index=False)
            self.assertEqual(run_pipeline(raw,out,skip_db=True),2)
            self.assertEqual(len(pd.read_csv(out)),2)

if __name__ == "__main__": unittest.main()
