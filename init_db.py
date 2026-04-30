from app.db import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            rol VARCHAR(50) NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Base de datos inicializada correctamente.")


if __name__ == "__main__":
    init_db()