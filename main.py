import logging
from telegram.ext import Application
from config.settings import TOKEN
from handlers.start_handler import get_handler as start_conv
from handlers.admin_handler import get_handlers as admin_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    app = Application.builder().token(TOKEN).build()

    # Start (ro‘yxatdan o‘tish)
    app.add_handler(start_conv())

    # Admin menyu
    for h in admin_handlers():
        app.add_handler(h)

    logger.info("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
