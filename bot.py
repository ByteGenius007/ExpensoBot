import telebot
from config import BOT_TOKEN
from logic import ExpenseManager
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)
manager = ExpenseManager()  

# Команда /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Привет! Я бот для учёта расходов.\nКоманды:\n/add — добавить трату\n/list — посмотреть список")

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
        date = datetime.now().strftime('%Y-%m-%d')
        manager.add_expense(message.from_user.id, category, amount, date)
        bot.send_message(message.chat.id, f"Сохранил: {category} — {amount} тг")
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
    for cat, amt, date in expenses:
        text += f"{date} — {cat}: {amt} тг\n"
    bot.send_message(message.chat.id, text)

# Запуск бота
bot.polling()
