import os
import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler

# Установите токен вашего бота
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Установите токен OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# Настройка OpenAI
openai.api_key = OPENAI_API_KEY

# Настройка логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для генерации сообщения про любовь
def generate_love_message() -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Generate a loving and inspiring message for a couple."}
            ],
            max_tokens=100
        )
        return response.choices[0].message['content'].strip()
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API Error: {e}")
        return "Something went wrong while generating the message."

# Функция для отправки сообщения в группу
async def send_love_message(context: ContextTypes.DEFAULT_TYPE) -> None:
    message = generate_love_message()
    await context.bot.send_message(chat_id=CHAT_ID, text=message)

# Функция для команды start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bot started! It will send love messages every 3 hours.")

# Основная функция
def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    scheduler = BackgroundScheduler()

    # Добавляем задачу для отправки сообщения каждые 3 часа
    scheduler.add_job(send_love_message, 'interval', hours=3, args=[application])
    scheduler.start()

    # Обработчик команды /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Запуск бота
    logger.info("Bot started and waiting for messages...")
    application.run_polling()

if __name__ == '__main__':
    main()
