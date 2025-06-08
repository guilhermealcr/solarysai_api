# Arquivo: solarys_api/app/database.py

import pyodbc
from . import config

def get_db_connection():

    conn = None
    try:
        # Nota: Não usamos autocommit=True aqui para termos controle sobre as transações.
        conn = pyodbc.connect(config.DATABASE_URL)
        yield conn
    except pyodbc.Error as ex:
        print(f"Erro de conexão com o banco de dados: {ex}")
    finally:
        if conn:
            conn.close()