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
    print('start: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(commands = ['showtoken'])
def show_token(message):
    if openai.api_key:
        bot.send_message(message.from_user.id, openai.api_key)
    else:
        bot.send_message(message.from_user.id, 'OpenAI токен API не установлен. Воспользуйтесь комадой /settoken или jghtltkbnt соответствующую переменную в окружении')


@bot.message_handler(commands = ['settoken'])
def set_token_dialog(message):
    bot.send_message(message.from_user.id, "Отлично! Установим новый API токен OpenAI\nОбращаю внимание, что старый токен будет перезаписан без возможности восстановления!\n\nДля установки нового токена отправьте мне его следующим сообщением.\nОжидаю токен...")
    bot.register_next_step_handler(message, set_new_token)
    print('settoken: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)


def set_new_token(message):
    if len(openai.api_key) == len(message.text):
        openai.api_key = message.text
        bot.send_message(message.from_user.id, "OpenAI токен API успешно изменен на " + message.text)
        print('token change success: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    else:
        bot.send_message(message.from_user.id, "Это непохоже на токен. Операция отменена!\nДля повторной попытки повторите команду '/settoken'")
        print('token change deny: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 "Вы можете отправлять запросы в OpenAI API через меня. Просто напишите мне свой запрос и я отправлю его на обработку.\n\nТакже доступные команды:\n\n/start - запуск бота\n/refresh - сбросить контекст(актуально, если получаете ошибку нехватки токенов)\n/help - вызов данной справки")
    print('help: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)

@bot.message_handler(commands=['refresh'])
def drop_cache(message):
    user_id = message.from_user.id

    cursor = conn.cursor()

    cursor.execute('DELETE FROM context WHERE user_id=?', (user_id,))

    context_cache.clear()

    conn.commit()
    bot.send_message(user_id, "Контекст и кэш очищены.")
    print('clear cash: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)

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
    print('bot accepted request from: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=context + message.text,
            temperature=0.5,
            max_tokens=3500
        )
        bot.reply_to(message, response.choices[0].text)
        print('bot replies to: ', message.from_user.id, message.from_user.first_name, message.from_user.last_name)

        # сохраняем контекст в кэше и базе данных
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO context (user_id, message, timestamp) VALUES (?, ?, ?)", (str(message.chat.id), context + message.text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        context_cache[message.chat.id] = {'message': context + message.text, 'timestamp': datetime.now()}

    except Exception as error:
        bot.reply_to(message, f"Произошла ошибка при обработке вашего запроса: {str(error)}")


print('L.A.P.S. GPT v1.0 started.')
# запускаем телеграм бота
bot.polling()

