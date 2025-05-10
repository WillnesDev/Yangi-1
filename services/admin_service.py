from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.permissions import check_admin
from utils.db_manager import add_admin, get_all_admins, remove_admin

# Conversation states
ADMIN_ID = 1

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin panelini ko'rsatish"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        if query:
            await query.answer()
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        else:
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📚 Kurslarni boshqarish", callback_data="manage_courses")
        ],
        [
            InlineKeyboardButton("👨‍🏫 O'qituvchilarni boshqarish", callback_data="manage_teachers")
        ],
        [
            InlineKeyboardButton("👨‍🎓 O'quvchilarni boshqarish", callback_data="manage_students")
        ],
        [
            InlineKeyboardButton("👥 Foydalanuvchilarni boshqarish", callback_data="manage_users")
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="show_dashboard")
        ],
        [
            InlineKeyboardButton("📝 Excel hisobotlar", callback_data="excel_reports")
        ],
        [
            InlineKeyboardButton("📨 Bildirishnomalar", callback_data="notification_panel")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.answer()
        await query.edit_message_text("Admin panel:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Admin panel:", reply_markup=reply_markup)

async def manage_users_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchilarni boshqarish panelini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("👨‍💼 Adminlarni boshqarish", callback_data="manage_admins")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Foydalanuvchilarni boshqarish:", reply_markup=reply_markup)

async def manage_admins_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Adminlarni boshqarish panelini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("➕ Admin qo'shish", callback_data="add_admin")
        ],
        [
            InlineKeyboardButton("➖ Adminni o'chirish", callback_data="remove_admin")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="manage_users")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Adminlarni boshqarish:", reply_markup=reply_markup)

async def add_admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin qo'shish uchun ID so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "Yangi admin ID raqamini kiriting:\n\n"
        "Masalan: 123456789"
    )
    
    return ADMIN_ID

async def add_admin_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin qo'shishni yakunlash"""
    try:
        admin_id = int(update.message.text.strip())
        
        # Admin qo'shish
        result = add_admin(admin_id)
        
        if result:
            await update.message.reply_text(f"Admin muvaffaqiyatli qo'shildi: {admin_id}")
        else:
            await update.message.reply_text(f"Bu foydalanuvchi allaqachon admin: {admin_id}")
        
        # Admin panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 Adminlar paneliga qaytish", callback_data="manage_admins")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Admin qo'shish yakunlandi.", reply_markup=reply_markup)
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Noto'g'ri format. Iltimos, raqam kiriting.\n\n"
            "Masalan: 123456789"
        )
        return ADMIN_ID

async def remove_admin_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin o'chirish uchun adminlar ro'yxatini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Adminlar ro'yxatini olish
    admins = get_all_admins()
    
    if not admins:
        await query.edit_message_text(
            "Adminlar ro'yxati bo'sh.\n\n"
            "Adminlar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for admin_id in admins:
        keyboard.append([InlineKeyboardButton(f"Admin ID: {admin_id}", callback_data=f"remove_admin_{admin_id}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_admins")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'chirish uchun adminni tanlang:", reply_markup=reply_markup)

async def remove_admin_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin o'chirishni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Admin ID'sini olish
    admin_id = int(query.data.split("_")[2])
    
    # Adminni o'chirish
    result = remove_admin(admin_id)
    
    if result:
        await query.edit_message_text(f"Admin muvaffaqiyatli o'chirildi: {admin_id}")
    else:
        await query.edit_message_text(f"Bu foydalanuvchi admin emas: {admin_id}")
    
    # Admin panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 Adminlar paneliga qaytish", callback_data="manage_admins")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Admin o'chirish yakunlandi.", reply_markup=reply_markup)