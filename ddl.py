import pandas as pd
import duckdb


SOURCE = "source/new/"
DB = 'my.db'
SHEETS = ["product_category_translation" , "products" , "sellers" , "customers" , "geolocation" , "orders" , "order_items" , "order_payments" , "order_reviews"]

def read_data(sheet_name: str) -> pd.DataFrame:
    df = pd.read_csv(f"{SOURCE}{sheet_name}.csv")
    return df

def create_table(table_name: str):
    query = f"queries/{table_name}.sql"
    
    with open(query) as f:
        sql = f.read()
    
    with duckdb.connect(DB) as duck:
        duck.execute(sql)
        duck.commit()
    
    with duckdb.connect(DB) as duck:
        duck.execute(f"truncate table {table_name}")
        duck.commit()

def load_data(df: pd.DataFrame, table_name: str):
    with duckdb.connect(DB) as duck:
        duck.execute(f"insert into {table_name} select * from df")
        duck.commit()
        print(table_name)

def pipeline():
    for sheet in SHEETS:
        print(f"Creating table {sheet}...")
        create_table(sheet)
        print(f"Loading data into {sheet}...")
        df = read_data(sheet)
        load_data(df, sheet)
        print(f"Table {sheet} is ready.")

pipeline()