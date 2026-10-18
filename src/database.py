from pathlib import Path
import sqlite3
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def build_database(tables,path=':memory:'):
    con=sqlite3.connect(str(path))
    con.executescript((ROOT/'sql/schema.sql').read_text())
    for name,df in tables.items():
        cols=','.join(df.columns); marks=','.join('?' for _ in df.columns)
        con.executemany(f'INSERT INTO {name} ({cols}) VALUES ({marks})',df.itertuples(index=False,name=None))
    con.commit()
    assert not con.execute('PRAGMA foreign_key_check').fetchall()
    return con

def load_tables(path):
    with sqlite3.connect(str(path)) as con:
        return {name:pd.read_sql_query(f'SELECT * FROM {name}',con) for name in ['institutions','campaigns','leads','events','enrollments']}
