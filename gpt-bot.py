import telebot
import openai
import os
import sqlite3
from datetime import datetime, timedelta

def init_env():
  # init env
  env_path = os.path.join(os.getcwd(), '.env')
  # Открываем файл и читаем все переменные окружения
  with open(env_path) as env:
      for line in env:
          # Удаляем пробелы по краям и разбиваем строку на две части по разделителю '='
          key, value = line.strip().split('=')
          # Устанавливаем переменную окружения
          os.environ[key] = value

# устанавливаем ключи API для TG и OpenAI из переменной окружения
init_env()
openai.api_key = os.environ["OPENAI_TOKEN"]
tg_token = os.environ["TG_TOKEN"]

# создаем экземпляр телеграм бота
bot = telebot.TeleBot(tg_token)

# создаем подключение к базе данных
conn = sqlite3.connect("example.db", check_same_thread=False)

# создаем таблицу в базе данных для хранения контекста
with conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS context (user_id TEXT, message TEXT, timestamp TEXT)")

# задаем интервал, через который массив с контекстом будет очищаться
CONTEXT_CACHE_INTERVAL = timedelta(minutes=10)

# словарь, в котором будут храниться последние запросы пользователя
context_cache = {}

# создаем обработчик команд
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 
                 "Привет! Я бот, который помогает вам общаться с OpenAI API.")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "Вы можете отправлять запросы в OpenAI API через меня. Просто напишите мне свой запрос и я отправлю его на обработку.")

# создаем обработчик сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    # смотрим, есть ли контекст в кэше
    if message.chat.id in context_cache and datetime.now() - context_cache[message.chat.id]['timestamp'] <= CONTEXT_CACHE_INTERVAL:
        context = context_cache[message.chat.id]['message']
    else:
        # если контекста в кэше нет, ищем его в базе данных
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT message FROM context WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (str(message.chat.id),))
            row = cur.fetchone()
            context = row[0] if row else ""

    bot.reply_to(message, "Запрос принят в работу.")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=context + message.text,
            temperature=0.5,
            max_tokens=3500
        )
        bot.reply_to(message, response.choices[0].text)

        # сохраняем контекст в кэше и базе данных
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO context (user_id, message, timestamp) VALUES (?, ?, ?)", (str(message.chat.id), context + message.text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        context_cache[message.chat.id] = {'message': context + message.text, 'timestamp': datetime.now()}

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке вашего запроса: {str(e)}")



# запускаем телеграм бота
bot.polling()