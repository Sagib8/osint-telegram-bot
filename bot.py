import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import BotCommand
from handlers import start, help_command, handle_text, handle_photo, handle_unsupported

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(~(filters.TEXT | filters.PHOTO), handle_unsupported))

    # Set bot commands before polling
    async def post_init(application):
        await application.bot.set_my_commands([
            BotCommand("start", "Start the bot and get basic instructions"),
            BotCommand("help", "Show what this bot can do"),
        ])

    # Assign the post-init hook
    app.post_init = post_init

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()