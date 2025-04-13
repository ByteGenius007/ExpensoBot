import sqlite3
from config import DB_NAME
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict


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
    
    def get_expenses_by_category(self, user_id, category):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT category, amount, date, time FROM expenses WHERE user_id = ? AND category = ? ORDER BY date DESC, time DESC",
            (user_id, category)
        )
        return cursor.fetchall()
    
    def get_daily_expenses(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT date, amount FROM expenses WHERE user_id = ?",
            (user_id,)
        )
        data = cursor.fetchall()

        daily = defaultdict(float)
        for date, amount in data:
            daily[date] += amount

        # сортировка по дате
        sorted_data = sorted(daily.items())
        return sorted_data

    def generate_daily_chart(self, user_id):
        data = self.get_daily_expenses(user_id)
        if not data:
            return None
        
        dates = [item[0] for item in data]
        amounts = [item[1] for item in data]

        plt.figure(figsize=(8, 5))
        plt.bar(dates, amounts, color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Дата')
        plt.ylabel('Сумма (тг)')
        plt.title('Расходы по дням')
        plt.tight_layout()

        path = f"chart_{user_id}.png"
        plt.savefig(path)
        plt.close()
        return path

