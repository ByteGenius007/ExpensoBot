import telebot
from config import BOT_TOKEN
from logic import ExpenseManager
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)
manager = ExpenseManager()

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id,
        "Привет! Я бот для учёта расходов.\n\n"
        "Команды:\n"
        "/add — добавить трату\n"
        "/list — список всех трат\n"
        "/delete — удалить трату по ID\n"
        "/stats — статистика по категориям\n"
        "/week — траты за неделю\n"
        "/month — траты за месяц"
    )

@bot.message_handler(commands=['add'])
def add_handler(message):
    bot.send_message(message.chat.id, "Напиши трату в формате: категория сумма (например: еда 500)")
    bot.register_next_step_handler(message, save_expense)

def save_expense(message):
    try:
        category, amount = message.text.split()
        amount = float(amount)
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')
        time = now.strftime('%H:%M:%S')
        manager.add_expense(message.from_user.id, category, amount, date, time)
        bot.send_message(message.chat.id, f"Сохранил: {category} — {amount} тг в {time}")
    except:
        bot.send_message(message.chat.id, "Ошибка! Напиши в формате: категория сумма")

@bot.message_handler(commands=['list'])
def list_handler(message):
    expenses = manager.get_expenses(message.from_user.id)
    if not expenses:
        bot.send_message(message.chat.id, "У тебя пока нет расходов.")
        return
    text = "Твои расходы:\n"
    for exp_id, cat, amt, date, time in expenses:
        text += f"{date} {time} — {cat}: {amt} тг (ID: {exp_id})\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['delete'])
def delete_handler(message):
    bot.send_message(message.chat.id, "Напиши ID траты, которую хочешь удалить:")
    bot.register_next_step_handler(message, delete_expense)

def delete_expense(message):
    try:
        expense_id = int(message.text)
        manager.delete_expense(message.from_user.id, expense_id)
        bot.send_message(message.chat.id, f"Трата с ID {expense_id} удалена.")
    except:
        bot.send_message(message.chat.id, "Ошибка! Напиши правильный ID.")

@bot.message_handler(commands=['stats'])
def stats_handler(message):
    stats = manager.get_category_stats(message.from_user.id)
    if not stats:
        bot.send_message(message.chat.id, "Нет данных для статистики.")
        return
    text = "Статистика по категориям:\n"
    for cat, total in stats:
        text += f"{cat}: {total} тг\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['week'])
def week_handler(message):
    data = manager.get_week_expenses(message.from_user.id)
    if not data:
        bot.send_message(message.chat.id, "За последнюю неделю трат нет.")
        return
    text = "Расходы за последнюю неделю:\n"
    for cat, amt, date, time in data:
        text += f"{date} {time} — {cat}: {amt} тг\n"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['month'])
def month_handler(message):
    data = manager.get_month_expenses(message.from_user.id)
    if not data:
        bot.send_message(message.chat.id, "В этом месяце трат пока нет.")
        return
    text = "Расходы за этот месяц:\n"
    for cat, amt, date, time in data:
        text += f"{date} {time} — {cat}: {amt} тг\n"
    bot.send_message(message.chat.id, text)

bot.polling()

