from telegram.ext import MessageHandler, filters

async def handle_unknown_message(update, context):
    """Noma'lum xabarlarni qayta ishlash"""
    await update.message.reply_text(
        "Noma'lum buyruq. Buyruqlar ro'yxatini ko'rish uchun /help buyrug'idan foydalaning."
    )

def register_message_handlers(application):
    """Barcha xabar handler'larini ro'yxatdan o'tkazish"""
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_unknown_message))