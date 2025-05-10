from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.permissions import check_admin
from utils.db_manager import (
    add_student, get_all_students, get_student_by_telegram_id, 
    update_student, delete_student, get_student_enrollments
)

# Conversation states
STUDENT_NAME, STUDENT_PHONE = range(2)
EDIT_STUDENT_NAME, EDIT_STUDENT_PHONE = range(2, 4)

async def manage_students_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchilarni boshqarish panelini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📋 O'quvchilar ro'yxati", callback_data="view_students")
        ],
        [
            InlineKeyboardButton("➕ O'quvchi qo'shish", callback_data="add_student")
        ],
        [
            InlineKeyboardButton("✏️ O'quvchini tahrirlash", callback_data="edit_student")
        ],
        [
            InlineKeyboardButton("🗑️ O'quvchini o'chirish", callback_data="delete_student")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'quvchilarni boshqarish:", reply_markup=reply_markup)

async def list_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchilar ro'yxatini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        students = get_all_students()
        
        if not students:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text("O'quvchilar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "O'quvchilar ro'yxati:\n\n"
        
        for student in students:
            message += f"👨‍🎓 {student['name']}\n"
            message += f"📞 Telefon: {student['phone']}\n"
            message += f"📅 Ro'yxatdan o'tgan sana: {student['registration_date']}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        students = get_all_students()
        
        if not students:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text("O'quvchilar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "O'quvchilar ro'yxati:\n\n"
        
        for student in students:
            message += f"👨‍🎓 {student['name']}\n"
            message += f"📞 Telefon: {student['phone']}\n"
            message += f"📅 Ro'yxatdan o'tgan sana: {student['registration_date']}\n\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

async def add_student_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchi qo'shish uchun o'quvchi nomini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "Yangi o'quvchi nomini kiriting:"
    )
    
    return STUDENT_NAME

async def add_student_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchi nomini saqlash va telefon raqamini so'rash"""
    context.user_data['student_name'] = update.message.text
    
    await update.message.reply_text(
        "O'quvchi telefon raqamini kiriting:"
    )
    
    return STUDENT_PHONE

async def add_student_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchi telefon raqamini saqlash va o'quvchini qo'shish"""
    context.user_data['student_phone'] = update.message.text
    
    # O'quvchini qo'shish
    student_id = add_student(
        update.effective_user.id,
        context.user_data['student_name'],
        context.user_data['student_phone']
    )
    
    if student_id:
        await update.message.reply_text(f"O'quvchi muvaffaqiyatli qo'shildi: {context.user_data['student_name']}")
    else:
        await update.message.reply_text("O'quvchi allaqachon mavjud.")
    
    # O'quvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'quvchilar paneliga qaytish", callback_data="manage_students")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("O'quvchi qo'shish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def edit_student_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tahrirlash uchun o'quvchini tanlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'quvchilar ro'yxatini olish
    students = get_all_students()
    
    if not students:
        await query.edit_message_text(
            "O'quvchilar ro'yxati bo'sh.\n\n"
            "O'quvchilar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for student in students:
        keyboard.append([InlineKeyboardButton(f"{student['name']}", callback_data=f"edit_student_{student['telegram_id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Tahrirlash uchun o'quvchini tanlang:", reply_markup=reply_markup)

async def edit_student_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchini tahrirlash uchun o'quvchi nomini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    # O'quvchi ID'sini olish
    student_id = int(query.data.split("_")[2])
    
    # O'quvchini olish
    student = get_student_by_telegram_id(student_id)
    
    if not student:
        await query.edit_message_text("O'quvchi topilmadi.")
        return ConversationHandler.END
    
    # O'quvchi ma'lumotlarini saqlash
    context.user_data['student_id'] = student_id
    context.user_data['student'] = student
    
    await query.edit_message_text(
        f"O'quvchi nomini tahrirlang:\n\n"
        f"Joriy nom: {student['name']}"
    )
    
    return EDIT_STUDENT_NAME

async def edit_student_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchi nomini saqlash va telefon raqamini so'rash"""
    context.user_data['new_student_name'] = update.message.text
    
    await update.message.reply_text(
        f"O'quvchi telefon raqamini tahrirlang:\n\n"
        f"Joriy telefon: {context.user_data['student']['phone']}"
    )
    
    return EDIT_STUDENT_PHONE

async def edit_student_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchi telefon raqamini saqlash va o'quvchini yangilash"""
    context.user_data['new_student_phone'] = update.message.text
    
    # O'quvchini yangilash
    result = update_student(
        context.user_data['student_id'],
        context.user_data['new_student_name'],
        context.user_data['new_student_phone']
    )
    
    if result:
        await update.message.reply_text(f"O'quvchi muvaffaqiyatli yangilandi: {context.user_data['new_student_name']}")
    else:
        await update.message.reply_text("O'quvchi yangilanmadi. O'quvchi topilmadi.")
    
    # O'quvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'quvchilar paneliga qaytish", callback_data="manage_students")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("O'quvchi tahrirlash yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def delete_student_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'chirish uchun o'quvchini tanlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'quvchilar ro'yxatini olish
    students = get_all_students()
    
    if not students:
        await query.edit_message_text(
            "O'quvchilar ro'yxati bo'sh.\n\n"
            "O'quvchilar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for student in students:
        keyboard.append([InlineKeyboardButton(f"{student['name']}", callback_data=f"delete_student_{student['telegram_id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_students")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'chirish uchun o'quvchini tanlang:", reply_markup=reply_markup)

async def delete_student_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchini o'chirishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # O'quvchi ID'sini olish
    student_id = int(query.data.split("_")[2])
    
    # O'quvchini olish
    student = get_student_by_telegram_id(student_id)
    
    if not student:
        await query.edit_message_text("O'quvchi topilmadi.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data=f"confirm_delete_student_{student_id}"),
            InlineKeyboardButton("❌ Yo'q", callback_data="cancel_delete_student")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Siz rostdan ham '{student['name']}' o'quvchisini o'chirmoqchimisiz?",
        reply_markup=reply_markup
    )

async def delete_student_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchini o'chirishni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    if query.data == "cancel_delete_student":
        # O'quvchilar boshqaruvi panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 O'quvchilar paneliga qaytish", callback_data="manage_students")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("O'quvchini o'chirish bekor qilindi.", reply_markup=reply_markup)
        return
    
    # O'quvchi ID'sini olish
    student_id = int(query.data.split("_")[3])
    
    # O'quvchini olish
    student = get_student_by_telegram_id(student_id)
    
    if not student:
        await query.edit_message_text("O'quvchi topilmadi.")
        return
    
    # O'quvchini o'chirish
    result = delete_student(student_id)
    
    if result:
        await query.edit_message_text(f"O'quvchi muvaffaqiyatli o'chirildi: {student['name']}")
    else:
        await query.edit_message_text("O'quvchi o'chirilmadi. O'quvchi topilmadi.")
    
    # O'quvchilar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 O'quvchilar paneliga qaytish", callback_data="manage_students")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'quvchi o'chirish yakunlandi.", reply_markup=reply_markup)

async def my_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi yozilgan kurslar ro'yxatini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
    else:
        user_id = update.effective_user.id
    
    # O'quvchini olish
    student = get_student_by_telegram_id(user_id)
    
    if not student:
        message = "Siz hali ro'yxatdan o'tmagansiz. Ro'yxatdan o'tish uchun /register buyrug'idan foydalaning."
        
        if query:
            await query.edit_message_text(message)
        else:
            await update.message.reply_text(message)
        return
    
    # O'quvchi yozilgan kurslarni olish
    enrollments = get_student_enrollments(user_id)
    
    if not enrollments:
        message = "Siz hali hech qanday kursga yozilmagansiz."
        
        keyboard = [[InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="view_courses_user")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if query:
            await query.edit_message_text(message, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message, reply_markup=reply_markup)
        return
    
    message = "Siz yozilgan kurslar:\n\n"
    
    for enrollment in enrollments:
        message += f"📚 {enrollment['course_name']}\n"
        message += f"📅 Yozilgan sana: {enrollment['enrollment_date']}\n\n"
    
    keyboard = [[InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="view_courses_user")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        await update.message.reply_text(message, reply_markup=reply_markup)

async def register_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ro'yxatdan o'tish uchun ism so'rash"""
    query = update.callback_query
    
    if query:
        await query.answer()
        await query.edit_message_text(
            "Ro'yxatdan o'tish uchun ismingizni kiriting:"
        )
    else:
        await update.message.reply_text(
            "Ro'yxatdan o'tish uchun ismingizni kiriting:"
        )
    
    return STUDENT_NAME

async def register_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ismni saqlash va telefon raqamini so'rash"""
    context.user_data['student_name'] = update.message.text
    
    await update.message.reply_text(
        "Telefon raqamingizni kiriting:"
    )
    
    return STUDENT_PHONE

async def register_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Telefon raqamini saqlash va ro'yxatdan o'tishni yakunlash"""
    context.user_data['student_phone'] = update.message.text
    
    # O'quvchini qo'shish
    student_id = add_student(
        update.effective_user.id,
        context.user_data['student_name'],
        context.user_data['student_phone']
    )
    
    if student_id:
        await update.message.reply_text(f"Siz muvaffaqiyatli ro'yxatdan o'tdingiz, {context.user_data['student_name']}!")
    else:
        await update.message.reply_text("Siz allaqachon ro'yxatdan o'tgansiz.")
    
    # Kurslar ro'yxatini ko'rsatish
    keyboard = [
        [InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="view_courses_user")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Ro'yxatdan o'tish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END