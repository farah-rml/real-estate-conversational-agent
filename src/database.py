import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return connection

def fetch_schema():
    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("select column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='properties';")
            res = curs.fetchall()
    return dict(res)

# TO-DO: et si query est une requête dangereuse générée par le LLM ?
def execute_query(query):
    with get_connection() as conn:
            with conn.cursor() as curs:
                curs.execute(query)
                res = curs.fetchall()
    return res 