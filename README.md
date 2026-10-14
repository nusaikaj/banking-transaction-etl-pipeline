# Banking Transaction ETL Pipeline

## Project Overview

This project is an end-to-end Data Engineering project that extracts raw banking transaction data from a CSV file, cleans and transforms the data using Python, loads the processed data into a MySQL database, and visualizes key insights using Power BI.

The main goal of this project is to demonstrate ETL pipeline development, data cleaning, MySQL database integration, and dashboard reporting.

## Technologies Used

- Python
- Pandas
- MySQL
- PyMySQL
- SQLAlchemy
- Power BI
- Git
- GitHub



```

## ETL Workflow

1. **Extract:** Read raw banking transaction data from the CSV file.
2. **Transform:** Clean and transform the data using Python and Pandas.
3. **Load:** Store the processed data in a MySQL database.
4. **Visualize:** Use Power BI to create dashboards and explore transaction insights.

## Project Folder Structure

```text
ETL PROJECT/
│
├── data/
│   ├── raw_transactions.csv
│   └── cleaned_transactions.csv
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── main.py
│
├── sql/
│   └── create_database.sql
│
├── dashboard/
│   └── banking_dashboard.pbix
│
├── README.md
├── requirements.txt
└── .gitignore
