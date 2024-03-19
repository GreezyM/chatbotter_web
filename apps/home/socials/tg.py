import os
from dotenv import load_dotenv
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
# from funcs import messages as msg

load_dotenv()
# Использование переменных окружения
token = os.getenv("TELEGRAM_BOT_TOKEN")
openai_secret = os.getenv("OPENAI_SECRET")

def ask_openai(messages):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_secret}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 1,
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при запросе к OpenAI: {e}")
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text_received = update.message.text
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Логирование сообщения от пользователя
    msg.log_message(chat_id=chat_id, user_id=user_id, message=text_received, sender_role="user")

    # Создание промпта и запрос к OpenAI
    messages = msg.create_messages(chat_id)

    response = ask_openai(messages=messages)
    if response:
        answer = response['choices'][0]['message']['content']
        bot_user_id = context.bot.id

        # Логирование ответа бота
        msg.log_message(chat_id=chat_id, user_id=bot_user_id, message=answer, sender_role="assistant")

        await update.message.reply_text(answer)  # Отправка ответа пользователю
