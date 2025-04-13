import sqlite3
from config import DB_NAME
from datetime import datetime, timedelta

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
                date TEXT,
                time TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_expense(self, user_id, category, amount, date, time):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (user_id, category, amount, date, time)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, amount, date, time))
        conn.commit()
        conn.close()

    def get_expenses(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, category, amount, date, time FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC, time DESC
        ''', (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_expense(self, user_id, expense_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM expenses WHERE user_id = ? AND id = ?
        ''', (user_id, expense_id))
        conn.commit()
        conn.close()

    def get_category_stats(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, SUM(amount) FROM expenses
            WHERE user_id = ?
            GROUP BY category
        ''', (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_week_expenses(self, user_id):
        date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, amount, date, time FROM expenses
            WHERE user_id = ? AND date >= ?
            ORDER BY date DESC, time DESC
        ''', (user_id, date_from))
        result = cursor.fetchall()
        conn.close()
        return result

    def get_month_expenses(self, user_id):
        today = datetime.now()
        month_start = today.replace(day=1).strftime('%Y-%m-%d')
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT category, amount, date, time FROM expenses
            WHERE user_id = ? AND date >= ?
            ORDER BY date DESC, time DESC
        ''', (user_id, month_start))
        result = cursor.fetchall()
        conn.close()
        return result


