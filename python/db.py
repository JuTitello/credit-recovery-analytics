import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    "> Abre a conexão com o PostgreSQL usando as variáveis do .env."

    conn = psycopg2.connect(

        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )
    cursor = conn.cursor()

    return conn, cursor