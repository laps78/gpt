import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

telegram_token = "5861663546:AAGnq_GEdjeFkfLI2Mz21PUPUF-6czDg0FI"
openai_token = "sk-z3d3UKtsWqVmhbBvN9UT3BlbkFJPr1cDyIBeCCMZKf1Kw4k"
channel_id = "CHANNEL_ID"
openai.api_key = openai_token

def start(update, context):
    # Перед использованием пишем юзеру, чтобы он подписался
    context.bot.send_message(chat_id = update.message.chat_id, text = "для использования бота необходимо подписаться на канал!")

def reply(update, context):
    # Получаем текст сообщения от пользователя
    message_text = update.message.text
    
    # проверяем, подписан ли пользователь на канал
    if not
    is_subscribed(update.message.chat_id):
        # просьба подписаться
        context.bot.send_message(chat_id = update.message.chat_id, text = "Для использования бота необходимо подписаться на канал")
        return
