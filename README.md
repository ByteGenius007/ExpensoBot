

## 📝 `README.md`

```markdown
# 🤖 Telegram бот для учёта расходов

Простой бот на Python, который помогает отслеживать личные траты прямо в Telegram. Сохраняет расходы в базу данных SQLite, показывает статистику, расходы по дням, неделе и месяцу.

## 🚀 Возможности

- Добавление трат (категория + сумма)
- Просмотр всех расходов
- Удаление трат по ID
- Статистика по категориям
- Расходы за неделю / месяц
- Отображение даты и времени каждой траты

## 🛠️ Технологии

- Python 3
- Библиотека `telebot` (pyTelegramBotAPI)
- SQLite (встроенная база данных)

## 📂 Структура проекта

```
├── bot.py            # основной файл бота
├── config.py         # файл с токеном Telegram-бота
├── logic.py          # логика работы с базой данных
└── expenses.db       # база данных SQLite (создаётся автоматически)
```

## ⚙️ Установка

1. Склонируй репозиторий:
   ```
   git clone https://github.com/ByteGenius007/ExpensoBot.git
   ```

2. Установи зависимости:
   ```
   pip install pyTelegramBotAPI
   ```

3. Создай файл `config.py`:
   ```python
   BOT_TOKEN = "твой_токен_от_бота"
   ```

4. Запусти бота:
   ```
   python bot.py
   ```

## 📌 Примеры команд в Telegram

- `/add` — добавить трату (например: еда 500)
- `/list` — список трат
- `/delete` — удалить трату по ID
- `/stats` — статистика по категориям
- `/week` — расходы за последнюю неделю
- `/month` — расходы за месяц

## 📬 Связь

Если есть вопросы или идеи — пиши :)

---

> Сделано с ❤️ на Python
