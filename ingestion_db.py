# ingestion_db.py

import os
import time
import logging
import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String

os.makedirs("logs", exist_ok=True)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, con):
    '''Ingest a dataframe into a database table'''
    df.to_sql(table_name, con=con, if_exists='replace', index=False)

def load_raw_data():
    '''Load CSVs from vendor_data_da folder and ingest into DB'''
    start = time.time()
    for file in os.listdir('vendor_data_da'):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join('vendor_data_da', file))
            logging.info(f'Ingesting {file} into db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start) / 60
    logging.info('----------Ingestion Complete----------')
    logging.info(f'Total Time Taken: {total_time:.2f} minutes')

if __name__ == "__main__":
    load_raw_data()