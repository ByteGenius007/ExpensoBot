import telebot
from config import BOT_TOKEN
from logic import ExpenseManager
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)
manager = ExpenseManager()

# Команда /start
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
        "/month — траты за месяц\n"
        "/help — помощь по использованию"
    )

# Команда /help
@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id,
        "Я бот для учёта твоих расходов.\n\n"
        "Вот список команд:\n"
        "/add — добавляет новую трату. Напиши категорию и сумму (например: еда 500).\n"
        "/list — показывает все твои траты с временем и датой.\n"
        "/delete — удаляет трату. Напиши ID нужной траты для удаления.\n"
        "/stats — выводит статистику по категориям расходов (сколько в сумме потрачено по каждой категории).\n"
        "/week — показывает траты за последние 7 дней и общую сумму.\n"
        "/month — показывает траты за текущий месяц и общую сумму.\n"
    )

# Команда /add
@bot.message_handler(commands=['add'])
def add_handler(message):
    bot.send_message(message.chat.id, "Напиши трату в формате: категория сумма (например: еда 500)")
    bot.register_next_step_handler(message, save_expense)

# Обработка траты
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

# Команда /list
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

# Команда /delete
@bot.message_handler(commands=['delete'])
def delete_handler(message):
    expenses = manager.get_expenses(message.from_user.id)
    if not expenses:
        bot.send_message(message.chat.id, "У тебя пока нет расходов, нечего удалять.")
        return
    
    text = "Вот твои траты:\n"
    for exp_id, cat, amt, date, time in expenses:
        text += f"ID: {exp_id} — {date} {time} — {cat}: {amt} тг\n"
    text += "\nНапиши ID траты, которую хочешь удалить:"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, delete_expense)

def delete_expense(message):
    try:
        expense_id = int(message.text)
        manager.delete_expense(message.from_user.id, expense_id)
        bot.send_message(message.chat.id, f"✅ Трата с ID {expense_id} удалена.")
    except:
        bot.send_message(message.chat.id, "⚠️ Ошибка! Напиши правильный ID.")

# Команда /stats
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

# Команда /week
@bot.message_handler(commands=['week'])
def week_handler(message):
    data = manager.get_week_expenses(message.from_user.id)
    if not data:
        bot.send_message(message.chat.id, "За последнюю неделю трат нет.")
        return
    total_week = sum([amt for _, amt, _, _ in data])
    text = "Расходы за последнюю неделю:\n"
    for cat, amt, date, time in data:
        text += f"{date} {time} — {cat}: {amt} тг\n"
    text += f"\nОбщая сумма: {total_week} тг"
    bot.send_message(message.chat.id, text)

# Команда /month
@bot.message_handler(commands=['month'])
def month_handler(message):
    data = manager.get_month_expenses(message.from_user.id)
    if not data:
        bot.send_message(message.chat.id, "В этом месяце трат пока нет.")
        return
    total_month = sum([amt for _, amt, _, _ in data])
    text = "Расходы за этот месяц:\n"
    for cat, amt, date, time in data:
        text += f"{date} {time} — {cat}: {amt} тг\n"
    text += f"\nОбщая сумма: {total_month} тг"
    bot.send_message(message.chat.id, text)

bot.polling()

