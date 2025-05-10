from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.permissions import check_admin
from utils.db_manager import add_teacher, get_all_teachers, get_teacher_by_id, update_teacher, delete_teacher

# Conversation states
TEACHER_NAME, TEACHER_SUBJECT, TEACHER_EXPERIENCE, TEACHER_CONTACT = range(4)
EDIT_TEACHER_NAME, EDIT_TEACHER_SUBJECT, EDIT_TEACHER_EXPERIENCE, EDIT_TEACHER_CONTACT = range(4, 8)

async def manage_teachers_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilarni boshqarish panelini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📋 O'qituvchilar ro'yxati", callback_data="view_teachers")
        ],
        [
            InlineKeyboardButton("➕ O'qituvchi qo'shish", callback_data="add_teacher")
        ],
        [
            InlineKeyboardButton("✏️ O'qituvchini tahrirlash", callback_data="edit_teacher")
        ],
        [
            InlineKeyboardButton("🗑️ O'qituvchini o'chirish", callback_data="delete_teacher")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'qituvchilarni boshqarish:", reply_markup=reply_markup)

async def list_teachers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilar ro'yxatini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        teachers = get_all_teachers()
        
        if not teachers:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text("O'qituvchilar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "O'qituvchilar ro'yxati:\n\n"
        
        for teacher in teachers:
            message += f"👨‍🏫 {teacher['name']}\n"
            message += f"📚 Fan: {teacher['subject']}\n"
            message += f"⏱️ Tajriba: {teacher['experience']}\n"
            message += f"📞 Aloqa: {teacher['contact']}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        teachers = get_all_teachers()
        
        if not teachers:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text("O'qituvchilar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "O'qituvchilar ro'yxati:\n\n"
        
        for teacher in teachers:
            message += f"👨‍🏫 {teacher['name']}\n"
            message += f"📚 Fan: {teacher['subject']}\n"
            message += f"⏱️ Tajriba: {teacher['experience']}\n"
            message += f"📞 Aloqa: {teacher['contact']}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

async def add_teacher_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi qo'shish uchun o'qituvchi nomini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "Yangi o'qituvchi nomini kiriting:"
    )
    
    return TEACHER_NAME

async def add_teacher_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi nomini saqlash va fanini so'rash"""
    context.user_data['teacher_name'] = update.message.text
    
    await update.message.reply_text(
        "O'qituvchi fanini kiriting:"
    )
    
    return TEACHER_SUBJECT

async def add_teacher_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi fanini saqlash va tajribasini so'rash"""
    context.user_data['teacher_subject'] = update.message.text
    
    await update.message.reply_text(
        "O'qituvchi tajribasini kiriting (masalan, 5 yil):"
    )
    
    return TEACHER_EXPERIENCE

async def add_teacher_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi tajribasini saqlash va aloqa ma'lumotlarini so'rash"""
    context.user_data['teacher_experience'] = update.message.text
    
    await update.message.reply_text(
        "O'qituvchi aloqa ma'lumotlarini kiriting (telefon raqami):"
    )
    
    return TEACHER_CONTACT

async def add_teacher_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi aloqa ma'lumotlarini saqlash va o'qituvchini qo'shish"""
    context.user_data['teacher_contact'] = update.message.text
    
    # O'qituvchini qo'shish
    teacher_id = add_teacher(
        context.user_data['teacher_name'],
        context.user_data['teacher_subject'],
        context.user_data['teacher_experience'],
        context.user_data['teacher_contact']
    )
    
    await update.message.reply_text(f"O'qituvchi muvaffaqiyatli qo'shildi: {context.user_data['teacher_name']}")
    
    # O'qituvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'qituvchilar paneliga qaytish", callback_data="manage_teachers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("O'qituvchi qo'shish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def edit_teacher_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tahrirlash uchun o'qituvchini tanlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'qituvchilar ro'yxatini olish
    teachers = get_all_teachers()
    
    if not teachers:
        await query.edit_message_text(
            "O'qituvchilar ro'yxati bo'sh.\n\n"
            "O'qituvchilar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for teacher in teachers:
        keyboard.append([InlineKeyboardButton(f"{teacher['name']}", callback_data=f"edit_teacher_{teacher['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Tahrirlash uchun o'qituvchini tanlang:", reply_markup=reply_markup)

async def edit_teacher_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchini tahrirlash uchun o'qituvchi nomini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    # O'qituvchi ID'sini olish
    teacher_id = int(query.data.split("_")[2])
    
    # O'qituvchini olish
    teacher = get_teacher_by_id(teacher_id)
    
    if not teacher:
        await query.edit_message_text("O'qituvchi topilmadi.")
        return ConversationHandler.END
    
    # O'qituvchi ma'lumotlarini saqlash
    context.user_data['teacher_id'] = teacher_id
    context.user_data['teacher'] = teacher
    
    await query.edit_message_text(
        f"O'qituvchi nomini tahrirlang:\n\n"
        f"Joriy nom: {teacher['name']}"
    )
    
    return EDIT_TEACHER_NAME

async def edit_teacher_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi nomini saqlash va fanini so'rash"""
    context.user_data['new_teacher_name'] = update.message.text
    
    await update.message.reply_text(
        f"O'qituvchi fanini tahrirlang:\n\n"
        f"Joriy fan: {context.user_data['teacher']['subject']}"
    )
    
    return EDIT_TEACHER_SUBJECT

async def edit_teacher_subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi fanini saqlash va tajribasini so'rash"""
    context.user_data['new_teacher_subject'] = update.message.text
    
    await update.message.reply_text(
        f"O'qituvchi tajribasini tahrirlang:\n\n"
        f"Joriy tajriba: {context.user_data['teacher']['experience']}"
    )
    
    return EDIT_TEACHER_EXPERIENCE

async def edit_teacher_experience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi tajribasini saqlash va aloqa ma'lumotlarini so'rash"""
    context.user_data['new_teacher_experience'] = update.message.text
    
    await update.message.reply_text(
        f"O'qituvchi aloqa ma'lumotlarini tahrirlang:\n\n"
        f"Joriy aloqa: {context.user_data['teacher']['contact']}"
    )
    
    return EDIT_TEACHER_CONTACT

async def edit_teacher_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchi aloqa ma'lumotlarini saqlash va o'qituvchini yangilash"""
    context.user_data['new_teacher_contact'] = update.message.text
    
    # O'qituvchini yangilash
    result = update_teacher(
        context.user_data['teacher_id'],
        context.user_data['new_teacher_name'],
        context.user_data['new_teacher_subject'],
        context.user_data['new_teacher_experience'],
        context.user_data['new_teacher_contact']
    )
    
    if result:
        await update.message.reply_text(f"O'qituvchi muvaffaqiyatli yangilandi: {context.user_data['new_teacher_name']}")
    else:
        await update.message.reply_text("O'qituvchi yangilanmadi. O'qituvchi topilmadi.")
    
    # O'qituvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'qituvchilar paneliga qaytish", callback_data="manage_teachers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("O'qituvchi tahrirlash yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def delete_teacher_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'chirish uchun o'qituvchini tanlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'qituvchilar ro'yxatini olish
    teachers = get_all_teachers()
    
    if not teachers:
        await query.edit_message_text(
            "O'qituvchilar ro'yxati bo'sh.\n\n"
            "O'qituvchilar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for teacher in teachers:
        keyboard.append([InlineKeyboardButton(f"{teacher['name']}", callback_data=f"delete_teacher_{teacher['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_teachers")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'chirish uchun o'qituvchini tanlang:", reply_markup=reply_markup)

async def delete_teacher_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchini o'chirishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'qituvchi ID'sini olish
    teacher_id = int(query.data.split("_")[2])
    
    # O'qituvchini olish
    teacher = get_teacher_by_id(teacher_id)
    
    if not teacher:
        await query.edit_message_text("O'qituvchi topilmadi.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data=f"confirm_delete_teacher_{teacher_id}"),
            InlineKeyboardButton("❌ Yo'q", callback_data="cancel_delete_teacher")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Siz rostdan ham '{teacher['name']}' o'qituvchisini o'chirmoqchimisiz?",
        reply_markup=reply_markup
    )

async def delete_teacher_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchini o'chirishni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    if query.data == "cancel_delete_teacher":
        # O'qituvchilar boshqaruvi panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 O'qituvchilar paneliga qaytish", callback_data="manage_teachers")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("O'qituvchini o'chirish bekor qilindi.", reply_markup=reply_markup)
        return
    
    # O'qituvchi ID'sini olish
    teacher_id = int(query.data.split("_")[3])
    
    # O'qituvchini olish
    teacher = get_teacher_by_id(teacher_id)
    
    if not teacher:
        await query.edit_message_text("O'qituvchi topilmadi.")
        return
    
    # O'qituvchini o'chirish
    result = delete_teacher(teacher_id)
    
    if result:
        await query.edit_message_text(f"O'qituvchi muvaffaqiyatli o'chirildi: {teacher['name']}")
    else:
        await query.edit_message_text("O'qituvchi o'chirilmadi. O'qituvchi topilmadi.")
    
    # O'qituvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'qituvchilar paneliga qaytish", callback_data="manage_teachers")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'qituvchi o'chirish yakunlandi.", reply_markup=reply_markup)