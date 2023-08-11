#/usr/bin/python3
import glob
import logging
import sys
from typing import Dict

import duckdb
import fire
from tqdm import tqdm


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def get_csv_tables(*, source_csv: str = 'data/source_csv') -> Dict[str, str]:

    logging.info(f"Getting tables from source directory... {source_csv}")
    files = glob.glob(f'{source_csv}/*.csv')
    tables = [file.split('/')[-1].split('.')[0] for file in files]

    return dict(zip(tables, files))


def ingest(*, tables: dict, db: str) -> str:

    logging.info(f"Ingesting {len(tables)} tables...")
    conn = duckdb.connect(database=db, read_only=False)
    try:
        for table, file in tqdm(tables.items(), position=0, leave=True):
            # logging.info(f'Ingesting {table} table from {file}...')
            conn.sql(f'DROP TABLE IF EXISTS {table}')
            conn.sql(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto('{file}')")
    except duckdb.CatalogException as exec:
        logging.Logger(exec, exec_info=True)
        raise
    finally:
        conn.close()

    return db


def main(*, source: str = 'data/source_csv', db: str = 'data/duck_sql.db'):
    tables = get_csv_tables(source_csv=source)
    db = ingest(tables=tables, db=db)
    logging.info(f"Database {db} created.")


if __name__ == "__main__":
    fire.Fire(main)
