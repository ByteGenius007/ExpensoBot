## 📝 `README`

# 🤖 Telegram бот для учёта расходов

Простой бот на Python, который помогает отслеживать личные траты прямо в Telegram. Сохраняет расходы в базу данных SQLite, показывает статистику, траты по дням, категориям, неделе и месяцу.

## 🚀 Возможности

- ➕ Добавление трат (категория + сумма)
- 📋 Просмотр всех расходов
- 🗑️ Удаление трат по ID
- 📊 Статистика по категориям
- 📆 Расходы за неделю / месяц
- 🕒 Отображение даты и времени каждой траты
- 🔎 Фильтр по категории (`/filter`)
- 📈 График расходов по дням (`/chart`)

## 🛠️ Технологии

- Python 3
- `pyTelegramBotAPI` (библиотека `telebot`)
- `matplotlib` (для графиков)
- SQLite (встроенная база данных)

## 📂 Структура проекта

```
├── bot.py            # основной файл бота
├── config.py         # файл с токеном Telegram-бота
├── logic.py          # логика работы с базой данных
├── expenses.db       # база данных SQLite (создаётся автоматически)
└── chart_USERID.png  # временный график (автоматически создаётся)
```

## ⚙️ Установка

1. Склонируй репозиторий:
   ```
   git clone https://github.com/ByteGenius007/ExpensoBot.git
   ```

2. Установи зависимости:
   ```
   pip install pyTelegramBotAPI matplotlib
   ```

3. Создай файл `config.py`:
   ```python
   BOT_TOKEN = "твой_токен_от_бота"
   DB_NAME = 'expenses.db'
   ```

4. Запусти бота:
   ```
   python bot.py
   ```

## 📬 Примеры команд в Telegram

- `/add` — добавить трату (например: еда 500)
- `/list` — список всех трат
- `/delete` — удалить трату по ID
- `/stats` — статистика по категориям
- `/week` — расходы за последнюю неделю
- `/month` — расходы за последний месяц
- `/filter` — фильтр по категории
- `/chart` — график расходов по дням
- `/help` — помощь и список команд

## 🧠 Идеи на будущее

- Лимиты и напоминания
- Ачивки за активность
- Экспорт в Excel/CSV
- Графики по категориям

---

> Сделано с ❤️ на Python и `matplotlib`
