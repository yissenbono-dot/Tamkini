import sqlite3
import bcrypt


def create_connection():
    return sqlite3.connect("tamkini.db")


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )
    return hashed_password.decode("utf-8")


def check_password(password, hashed_password):
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password_bytes, hashed_bytes)


if __name__ == "__main__":
    create_tables()
    print("Tamkini database is ready.")