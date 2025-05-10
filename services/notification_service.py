from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.permissions import check_admin
from utils.db_manager import get_all_students, get_all_courses, get_course_students, get_course_by_id, get_student_by_telegram_id

# Conversation states
NOTIFICATION_TEXT = 1

async def notification_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bildirishnomalar panelini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("📨 Barcha foydalanuvchilarga", callback_data="notify_all")
            ],
            [
                InlineKeyboardButton("📨 Kurs o'quvchilariga", callback_data="notify_course")
            ],
            [
                InlineKeyboardButton("📨 Bitta o'quvchiga", callback_data="notify_student")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("Bildirishnomalar paneli:", reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("📨 Barcha foydalanuvchilarga", callback_data="notify_all")
            ],
            [
                InlineKeyboardButton("📨 Kurs o'quvchilariga", callback_data="notify_course")
            ],
            [
                InlineKeyboardButton("📨 Bitta o'quvchiga", callback_data="notify_student")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Bildirishnomalar paneli:", reply_markup=reply_markup)

async def notify_all_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha foydalanuvchilarga bildirishnoma yuborish uchun matn so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "Barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni kiriting:"
    )
    
    return NOTIFICATION_TEXT

async def notify_all_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha foydalanuvchilarga bildirishnoma yuborishni yakunlash"""
    notification_text = update.message.text
    
    # Barcha o'quvchilarni olish
    students = get_all_students()
    
    if not students:
        await update.message.reply_text("O'quvchilar ro'yxati bo'sh.")
        
        # Bildirishnomalar paneliga qaytish
        keyboard = [
            [InlineKeyboardButton("🔙 Bildirishnomalar paneliga qaytish", callback_data="notification_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Bildirishnoma yuborish yakunlandi.", reply_markup=reply_markup)
        
        return ConversationHandler.END
    
    # Bildirishnomani yuborish
    success_count = 0
    fail_count = 0
    
    for student in students:
        try:
            await context.bot.send_message(
                chat_id=student['telegram_id'],
                text=notification_text
            )
            success_count += 1
        except Exception:
            fail_count += 1
    
    await update.message.reply_text(
        f"Bildirishnoma yuborildi:\n\n"
        f"✅ Muvaffaqiyatli: {success_count}\n"
        f"❌ Muvaffaqiyatsiz: {fail_count}"
    )
    
    # Bildirishnomalar paneliga qaytish
    keyboard = [
        [InlineKeyboardButton("🔙 Bildirishnomalar paneliga qaytish", callback_data="notification_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Bildirishnoma yuborish yakunlandi.", reply_markup=reply_markup)
    
    return ConversationHandler.END

async def notify_course_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs o'quvchilariga bildirishnoma yuborish uchun kursni tanlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurslar ro'yxatini olish
    courses = get_all_courses()
    
    if not courses:
        await query.edit_message_text(
            "Kurslar ro'yxati bo'sh.\n\n"
            "Bildirishnomalar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for course in courses:
        keyboard.append([InlineKeyboardButton(f"{course['name']}", callback_data=f"select_course_{course['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="notification_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Bildirishnoma yuborish uchun kursni tanlang:", reply_markup=reply_markup)

async def select_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursni tanlash va bildirishnoma matnini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[2])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return ConversationHandler.END
    
    # Kurs ID'sini saqlash
    context.user_data['course_id'] = course_id
    context.user_data['course_name'] = course['name']
    
    await query.edit_message_text(
        f"'{course['name']}' kursi o'quvchilariga yubormoqchi bo'lgan xabaringizni kiriting:"
    )
    
    return NOTIFICATION_TEXT

async def notify_course_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs o'quvchilariga bildirishnoma yuborishni yakunlash"""
    notification_text = update.message.text
    
    # Kurs o'quvchilarini olish
    students = get_course_students(context.user_data['course_id'])
    
    if not students:
        await update.message.reply_text(f"'{context.user_data['course_name']}' kursiga hech kim yozilmagan.")
        
        # Bildirishnomalar paneliga qaytish
        keyboard = [
            [InlineKeyboardButton("🔙 Bildirishnomalar paneliga qaytish", callback_data="notification_panel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Bildirishnoma yuborish yakunlandi.", reply_markup=reply_markup)
        
        # User data'ni tozalash
        context.user_data.clear()
        
        return ConversationHandler.END
    
    # Bildirishnomani yuborish
    success_count = 0
    fail_count = 0
    
    for student in students:
        try:
            await context.bot.send_message(
                chat_id=student['telegram_id'],
                text=notification_text
            )
            success_count += 1
        except Exception:
            fail_count += 1
    
    await update.message.reply_text(
        f"Bildirishnoma yuborildi:\n\n"
        f"✅ Muvaffaqiyatli: {success_count}\n"
        f"❌ Muvaffaqiyatsiz: {fail_count}"
    )
    
    # Bildirishnomalar paneliga qaytish
    keyboard = [
        [InlineKeyboardButton("🔙 Bildirishnomalar paneliga qaytish", callback_data="notification_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Bildirishnoma yuborish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def notify_student_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bitta o'quvchiga bildirishnoma yuborish uchun o'quvchini tanlash"""
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
            "Bildirishnomalar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for student in students:
        keyboard.append([InlineKeyboardButton(f"{student['name']}", callback_data=f"select_student_{student['telegram_id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="notification_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Bildirishnoma yuborish uchun o'quvchini tanlang:", reply_markup=reply_markup)

async def select_student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchini tanlash va bildirishnoma matnini so'rash"""
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
    
    # O'quvchi ID'sini saqlash
    context.user_data['student_id'] = student_id
    context.user_data['student_name'] = student['name']
    
    await query.edit_message_text(
        f"'{student['name']}' o'quvchisiga yubormoqchi bo'lgan xabaringizni kiriting:"
    )
    
    return NOTIFICATION_TEXT

async def notify_student_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bitta o'quvchiga bildirishnoma yuborishni yakunlash"""
    notification_text = update.message.text
    
    # Bildirishnomani yuborish
    try:
        await context.bot.send_message(
            chat_id=context.user_data['student_id'],
            text=notification_text
        )
        
        await update.message.reply_text(f"Bildirishnoma '{context.user_data['student_name']}' o'quvchisiga muvaffaqiyatli yuborildi.")
    except Exception as e:
        await update.message.reply_text(f"Bildirishnoma yuborilmadi. Xatolik: {str(e)}")
    
    # Bildirishnomalar paneliga qaytish
    keyboard = [
        [InlineKeyboardButton("🔙 Bildirishnomalar paneliga qaytish", callback_data="notification_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Bildirishnoma yuborish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END