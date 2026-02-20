import sqlite3

def create_transactions_table():
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            expense REAL,
            category TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()
