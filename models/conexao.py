import psycopg2
from psycopg2.extras import RealDictCursor

def conectar():

    return psycopg2.connect(
        host="localhost",
        database="cine_review",
        user="postgres",
        password="postgres",
        port="5432"
    )

def criar_cursor(conexao):

    return conexao.cursor(
        cursor_factory=RealDictCursor
    )