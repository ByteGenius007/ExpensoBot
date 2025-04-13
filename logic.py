import sqlite3
from config import DB_NAME

class ExpenseManager:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                amount REAL,
                date TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self, user_id, category, amount, date):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, category, amount, date)
            VALUES (?, ?, ?, ?)
        ''', (user_id, category, amount, date))
        conn.commit()
        conn.close()

    def get_expenses(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, amount, date FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC
        ''', (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result

