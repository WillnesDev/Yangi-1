import logging
import os
from telegram.ext import Application

from config.settings import BOT_TOKEN, DATA_DIR
from utils.db_manager import initialize_database
from handlers.command_handlers import register_command_handlers
from handlers.conversation_handlers import register_conversation_handlers
from handlers.callback_handlers import register_callback_handlers
from handlers.message_handlers import register_message_handlers

# Logging sozlamalari
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Botni ishga tushirish"""
    try:
        # Ma'lumotlar papkasini yaratish
        logger.info("Ma'lumotlar papkasini yaratish...")
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Ma'lumotlar bazasini yaratish
        logger.info("Ma'lumotlar bazasini yaratish...")
        initialize_database()
        
        # Bot yaratish
        logger.info("Botni yaratish...")
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Barcha handler'larni ro'yxatdan o'tkazish
        logger.info("Handler'larni ro'yxatdan o'tkazish...")
        register_command_handlers(application)
        register_conversation_handlers(application)
        register_callback_handlers(application)
        register_message_handlers(application)
        
        # Botni ishga tushirish
        logger.info("Bot ishga tushdi...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Xatolik yuz berdi: {e}")
        raise

if __name__ == "__main__":
    main()