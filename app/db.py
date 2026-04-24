import os
import psycopg2

def get_connection():
    database_url = os.environ.get("DATABASE_URL")
    return psycopg2.connect(database_url)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            rol VARCHAR(50) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()