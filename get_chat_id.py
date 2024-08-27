from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Chat ID: {chat_id}')

def main() -> None:
    TELEGRAM_BOT_TOKEN = "7456926092:AAF_HViZKbm1LxEyDuZ8OxnahT0wvjCF4y4"
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == "__main__":
    main()
