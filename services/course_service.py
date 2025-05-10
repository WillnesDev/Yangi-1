from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.permissions import check_admin
from utils.db_manager import (
    add_course, get_all_courses, get_course_by_id, update_course, 
    delete_course, get_student_by_telegram_id, enroll_student,
    get_all_teachers, assign_teacher_to_course, get_course_teacher,
    get_course_students, set_course_dates, set_course_max_students
)

# Conversation states
COURSE_NAME, COURSE_DESCRIPTION, COURSE_DURATION, COURSE_PRICE = range(4)
EDIT_COURSE_NAME, EDIT_COURSE_DESCRIPTION, EDIT_COURSE_DURATION, EDIT_COURSE_PRICE = range(4, 8)
COURSE_START_DATE, COURSE_END_DATE = range(8, 10)
COURSE_MAX_STUDENTS = 10

async def manage_courses_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurslarni boshqarish panelini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📋 Kurslar ro'yxati", callback_data="view_courses")
        ],
        [
            InlineKeyboardButton("➕ Kurs qo'shish", callback_data="add_course")
        ],
        [
            InlineKeyboardButton("✏️ Kursni tahrirlash", callback_data="edit_course")
        ],
        [
            InlineKeyboardButton("🗑️ Kursni o'chirish", callback_data="delete_course")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Kurslarni boshqarish:", reply_markup=reply_markup)

async def list_courses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurslar ro'yxatini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        courses = get_all_courses()
        
        if not courses:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text("Kurslar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "Kurslar ro'yxati:\n\n"
        
        for course in courses:
            message += f"📚 {course['name']}\n"
            message += f"📝 {course['description']}\n"
            message += f"⏱️ Davomiyligi: {course['duration']}\n"
            message += f"💰 Narxi: {course['price']}\n"
            
            if course['teacher_id']:
                teacher = get_course_teacher(course['id'])
                if teacher:
                    message += f"👨‍🏫 O'qituvchi: {teacher['name']}\n"
            
            if course['start_date'] and course['end_date']:
                message += f"📅 Boshlanish: {course['start_date']}\n"
                message += f"📅 Tugash: {course['end_date']}\n"
            
            message += f"👨‍🎓 Maksimal o'quvchilar soni: {course['max_students']}\n"
            message += f"🔍 Batafsil: /course_{course['id']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔍 Kurs tafsilotlari", callback_data=f"course_details_{courses[0]['id']}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        courses = get_all_courses()
        
        if not courses:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text("Kurslar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "Kurslar ro'yxati:\n\n"
        
        for course in courses:
            message += f"📚 {course['name']}\n"
            message += f"📝 {course['description']}\n"
            message += f"⏱️ Davomiyligi: {course['duration']}\n"
            message += f"💰 Narxi: {course['price']}\n"
            
            if course['teacher_id']:
                teacher = get_course_teacher(course['id'])
                if teacher:
                    message += f"👨‍🏫 O'qituvchi: {teacher['name']}\n"
            
            if course['start_date'] and course['end_date']:
                message += f"📅 Boshlanish: {course['start_date']}\n"
                message += f"📅 Tugash: {course['end_date']}\n"
            
            message += f"👨‍🎓 Maksimal o'quvchilar soni: {course['max_students']}\n"
            message += f"🔍 Batafsil: /course_{course['id']}\n\n"
        
        keyboard = [
            [InlineKeyboardButton("🔍 Kurs tafsilotlari", callback_data=f"course_details_{courses[0]['id']}")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

async def add_course_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs qo'shish uchun kurs nomini so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    await query.edit_message_text(
        "Yangi kurs nomini kiriting:"
    )
    
    return COURSE_NAME

async def add_course_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs nomini saqlash va tavsifini so'rash"""
    context.user_data['course_name'] = update.message.text
    
    await update.message.reply_text(
        "Kurs tavsifini kiriting:"
    )
    
    return COURSE_DESCRIPTION

async def add_course_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tavsifini saqlash va davomiyligini so'rash"""
    context.user_data['course_description'] = update.message.text
    
    await update.message.reply_text(
        "Kurs davomiyligini kiriting (masalan, 3 oy):"
    )
    
    return COURSE_DURATION

async def add_course_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs davomiyligini saqlash va narxini so'rash"""
    context.user_data['course_duration'] = update.message.text
    
    await update.message.reply_text(
        "Kurs narxini kiriting (masalan, 1000000):"
    )
    
    return COURSE_PRICE

async def add_course_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs narxini saqlash va kursni qo'shish"""
    try:
        price = update.message.text
        
        # Kursni qo'shish
        course_id = add_course(
            context.user_data['course_name'],
            context.user_data['course_description'],
            context.user_data['course_duration'],
            price
        )
        
        await update.message.reply_text(f"Kurs muvaffaqiyatli qo'shildi: {context.user_data['course_name']}")
        
        # Kurslar boshqaruvi panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 Kurslar paneliga qaytish", callback_data="manage_courses")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Kurs qo'shish yakunlandi.", reply_markup=reply_markup)
        
        # User data'ni tozalash
        context.user_data.clear()
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Noto'g'ri format. Iltimos, raqam kiriting.\n\n"
            "Masalan: 1000000"
        )
        return COURSE_PRICE

async def edit_course_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tahrirlash uchun kursni tanlash"""
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
            "Kurslar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for course in courses:
        keyboard.append([InlineKeyboardButton(f"{course['name']}", callback_data=f"edit_course_{course['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Tahrirlash uchun kursni tanlang:", reply_markup=reply_markup)

async def edit_course_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursni tahrirlash uchun kurs nomini so'rash"""
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
    
    # Kurs ma'lumotlarini saqlash
    context.user_data['course_id'] = course_id
    context.user_data['course'] = course
    
    await query.edit_message_text(
        f"Kurs nomini tahrirlang:\n\n"
        f"Joriy nom: {course['name']}"
    )
    
    return EDIT_COURSE_NAME

async def edit_course_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs nomini saqlash va tavsifini so'rash"""
    context.user_data['new_course_name'] = update.message.text
    
    await update.message.reply_text(
        f"Kurs tavsifini tahrirlang:\n\n"
        f"Joriy tavsif: {context.user_data['course']['description']}"
    )
    
    return EDIT_COURSE_DESCRIPTION

async def edit_course_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tavsifini saqlash va davomiyligini so'rash"""
    context.user_data['new_course_description'] = update.message.text
    
    await update.message.reply_text(
        f"Kurs davomiyligini tahrirlang:\n\n"
        f"Joriy davomiylik: {context.user_data['course']['duration']}"
    )
    
    return EDIT_COURSE_DURATION

async def edit_course_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs davomiyligini saqlash va narxini so'rash"""
    context.user_data['new_course_duration'] = update.message.text
    
    await update.message.reply_text(
        f"Kurs narxini tahrirlang:\n\n"
        f"Joriy narx: {context.user_data['course']['price']}"
    )
    
    return EDIT_COURSE_PRICE

async def edit_course_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs narxini saqlash va kursni yangilash"""
    try:
        price = update.message.text
        
        # Kursni yangilash
        result = update_course(
            context.user_data['course_id'],
            context.user_data['new_course_name'],
            context.user_data['new_course_description'],
            context.user_data['new_course_duration'],
            price
        )
        
        if result:
            await update.message.reply_text(f"Kurs muvaffaqiyatli yangilandi: {context.user_data['new_course_name']}")
        else:
            await update.message.reply_text("Kurs yangilanmadi. Kurs topilmadi.")
        
        # Kurslar boshqaruvi panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 Kurslar paneliga qaytish", callback_data="manage_courses")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Kurs tahrirlash yakunlandi.", reply_markup=reply_markup)
        
        # User data'ni tozalash
        context.user_data.clear()
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Noto'g'ri format. Iltimos, raqam kiriting.\n\n"
            "Masalan: 1000000"
        )
        return EDIT_COURSE_PRICE

async def delete_course_select(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'chirish uchun kursni tanlash"""
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
            "Kurslar paneliga qaytish uchun /admin buyrug'idan foydalaning."
        )
        return
    
    keyboard = []
    
    for course in courses:
        keyboard.append([InlineKeyboardButton(f"{course['name']}", callback_data=f"delete_course_{course['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="manage_courses")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'chirish uchun kursni tanlang:", reply_markup=reply_markup)

async def delete_course_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursni o'chirishni tasdiqlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[2])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Ha", callback_data=f"confirm_delete_course_{course_id}"),
            InlineKeyboardButton("❌ Yo'q", callback_data="cancel_delete_course")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"Siz rostdan ham '{course['name']}' kursini o'chirmoqchimisiz?",
        reply_markup=reply_markup
    )

async def delete_course_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursni o'chirishni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    if query.data == "cancel_delete_course":
        # Kurslar boshqaruvi panelini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 Kurslar paneliga qaytish", callback_data="manage_courses")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("Kursni o'chirish bekor qilindi.", reply_markup=reply_markup)
        return
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[3])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    # Kursni o'chirish
    result = delete_course(course_id)
    
    if result:
        await query.edit_message_text(f"Kurs muvaffaqiyatli o'chirildi: {course['name']}")
    else:
        await query.edit_message_text("Kurs o'chirilmadi. Kurs topilmadi.")
    
    # Kurslar boshqaruvi panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 Kurslar paneliga qaytish", callback_data="manage_courses")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Kurs o'chirish yakunlandi.", reply_markup=reply_markup)

async def view_courses_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchilar uchun kurslar ro'yxatini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        
        courses = get_all_courses()
        
        if not courses:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text("Kurslar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "Mavjud kurslar ro'yxati:\n\n"
        
        for course in courses:
            message += f"📚 {course['name']}\n"
            message += f"📝 {course['description']}\n"
            message += f"⏱️ Davomiyligi: {course['duration']}\n"
            message += f"💰 Narxi: {course['price']}\n"
            
            if course['teacher_id']:
                teacher = get_course_teacher(course['id'])
                if teacher:
                    message += f"👨‍🏫 O'qituvchi: {teacher['name']}\n"
            
            if course['start_date'] and course['end_date']:
                message += f"📅 Boshlanish: {course['start_date']}\n"
                message += f"📅 Tugash: {course['end_date']}\n"
            
            message += f"👨‍🎓 Maksimal o'quvchilar soni: {course['max_students']}\n"
            message += f"🔍 Batafsil: /course_{course['id']}\n\n"
        
        keyboard = []
        
        for course in courses:
            keyboard.append([InlineKeyboardButton(f"✅ {course['name']}ga yozilish", callback_data=f"enroll_{course['id']}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        courses = get_all_courses()
        
        if not courses:
            keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text("Kurslar ro'yxati bo'sh.", reply_markup=reply_markup)
            return
        
        message = "Mavjud kurslar ro'yxati:\n\n"
        
        for course in courses:
            message += f"📚 {course['name']}\n"
            message += f"📝 {course['description']}\n"
            message += f"⏱️ Davomiyligi: {course['duration']}\n"
            message += f"💰 Narxi: {course['price']}\n"
            
            if course['teacher_id']:
                teacher = get_course_teacher(course['id'])
                if teacher:
                    message += f"👨‍🏫 O'qituvchi: {teacher['name']}\n"
            
            if course['start_date'] and course['end_date']:
                message += f"📅 Boshlanish: {course['start_date']}\n"
                message += f"📅 Tugash: {course['end_date']}\n"
            
            message += f"👨‍🎓 Maksimal o'quvchilar soni: {course['max_students']}\n"
            message += f"🔍 Batafsil: /course_{course['id']}\n\n"
        
        keyboard = []
        
        for course in courses:
            keyboard.append([InlineKeyboardButton(f"✅ {course['name']}ga yozilish", callback_data=f"enroll_{course['id']}")])
        
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

async def enroll_course(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursga yozilish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[1])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    # O'quvchini olish
    student = get_student_by_telegram_id(user_id)
    
    if not student:
        keyboard = [
            [InlineKeyboardButton("✅ Ro'yxatdan o'tish", callback_data="register")],
            [InlineKeyboardButton("🔙 Orqaga", callback_data="view_courses_user")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Kursga yozilish uchun avval ro'yxatdan o'tishingiz kerak.",
            reply_markup=reply_markup
        )
        return
    
    # Kursga yozilish
    result = enroll_student(user_id, course_id, course['name'])
    
    if result:
        await query.edit_message_text(f"Siz muvaffaqiyatli '{course['name']}' kursiga yozildingiz.")
    else:
        await query.edit_message_text(f"Siz allaqachon '{course['name']}' kursiga yozilgansiz.")
    
    # Kurslar ro'yxatini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 Kurslar ro'yxatiga qaytish", callback_data="view_courses_user")],
        [InlineKeyboardButton("📋 Mening kurslarim", callback_data="my_courses")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("Kursga yozilish yakunlandi.", reply_markup=reply_markup)

async def course_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs tafsilotlarini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[2])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    message = f"📚 {course['name']}\n"
    message += f"📝 {course['description']}\n"
    message += f"⏱️ Davomiyligi: {course['duration']}\n"
    message += f"💰 Narxi: {course['price']}\n"
    
    if course['teacher_id']:
        teacher = get_course_teacher(course_id)
        if teacher:
            message += f"👨‍🏫 O'qituvchi: {teacher['name']}\n"
    else:
        message += "👨‍🏫 O'qituvchi: tayinlanmagan\n"
    
    if course['start_date'] and course['end_date']:
        message += f"📅 Boshlanish: {course['start_date']}\n"
        message += f"📅 Tugash: {course['end_date']}\n"
    else:
        message += "📅 Sana: belgilanmagan\n"
    
    message += f"👨‍🎓 Maksimal o'quvchilar soni: {course['max_students']}\n"
    
    # Kursga yozilgan o'quvchilar sonini olish
    students = get_course_students(course_id)
    message += f"👨‍🎓 Yozilgan o'quvchilar soni: {len(students)}\n"
    
    keyboard = [
        [
            InlineKeyboardButton("👨‍🏫 O'qituvchi tayinlash", callback_data=f"assign_teacher_{course_id}"),
            InlineKeyboardButton("📅 Sana belgilash", callback_data=f"set_dates_{course_id}")
        ],
        [
            InlineKeyboardButton("👨‍🎓 O'quvchilar soni", callback_data=f"set_max_students_{course_id}"),
            InlineKeyboardButton("👨‍🎓 O'quvchilar ro'yxati", callback_data=f"course_students_{course_id}")
        ],
        [
            InlineKeyboardButton("📊 Excel hisobot", callback_data=f"excel_course_students_{course_id}")
        ],
        [
            InlineKeyboardButton("🔙 Orqaga", callback_data="view_courses")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def assign_teacher_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursga o'qituvchi tayinlash uchun o'qituvchilar ro'yxatini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[2])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    # O'qituvchilar ro'yxatini olish
    teachers = get_all_teachers()
    
    if not teachers:
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data=f"course_details_{course_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "O'qituvchilar ro'yxati bo'sh. Avval o'qituvchi qo'shing.",
            reply_markup=reply_markup
        )
        return
    
    keyboard = []
    
    for teacher in teachers:
        keyboard.append([InlineKeyboardButton(f"{teacher['name']}", callback_data=f"select_teacher_{course_id}_{teacher['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data=f"course_details_{course_id}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"'{course['name']}' kursi uchun o'qituvchini tanlang:",
        reply_markup=reply_markup
    )

async def select_teacher_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchini tanlashni yakunlash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurs va o'qituvchi ID'larini olish
    data = query.data.split("_")
    course_id = int(data[2])
    teacher_id = int(data[3])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    # O'qituvchini olish
    teacher = get_teacher_by_id(teacher_id)
    
    if not teacher:
        await query.edit_message_text("O'qituvchi topilmadi.")
        return
    
    # O'qituvchini kursga tayinlash
    result = assign_teacher_to_course(course_id, teacher_id)
    
    if result:
        await query.edit_message_text(f"'{teacher['name']}' o'qituvchisi '{course['name']}' kursiga muvaffaqiyatli tayinlandi.")
    else:
        await query.edit_message_text("O'qituvchi tayinlanmadi. Kurs topilmadi.")
    
    # Kurs tafsilotlarini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 Kurs tafsilotlariga qaytish", callback_data=f"course_details_{course_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text("O'qituvchi tayinlash yakunlandi.", reply_markup=reply_markup)

async def course_students_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursga yozilgan o'quvchilar ro'yxatini ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[2])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return
    
    # Kursga yozilgan o'quvchilar ro'yxatini olish
    students = get_course_students(course_id)
    
    if not students:
        keyboard = [[InlineKeyboardButton("🔙 Orqaga", callback_data=f"course_details_{course_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"'{course['name']}' kursiga hech kim yozilmagan.",
            reply_markup=reply_markup
        )
        return
    
    message = f"'{course['name']}' kursiga yozilgan o'quvchilar:\n\n"
    
    for i, student in enumerate(students, 1):
        message += f"{i}. {student['name']} - {student['phone']}\n"
        message += f"   Yozilgan sana: {student['enrollment_date']}\n\n"
    
    keyboard = [
        [InlineKeyboardButton("📊 Excel hisobot", callback_data=f"excel_course_students_{course_id}")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data=f"course_details_{course_id}")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def set_dates_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs boshlanish va tugash sanalarini o'rnatish uchun boshlanish sanasini so'rash"""
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
    
    await query.edit_message_text(
        f"'{course['name']}' kursi uchun boshlanish sanasini kiriting (YYYY-MM-DD formatida):"
    )
    
    return COURSE_START_DATE

async def set_start_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Boshlanish sanasini saqlash va tugash sanasini so'rash"""
    context.user_data['start_date'] = update.message.text
    
    # Kursni olish
    course = get_course_by_id(context.user_data['course_id'])
    
    await update.message.reply_text(
        f"'{course['name']}' kursi uchun tugash sanasini kiriting (YYYY-MM-DD formatida):"
    )
    
    return COURSE_END_DATE

async def set_end_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tugash sanasini saqlash va kurs sanalarini o'rnatish"""
    end_date = update.message.text
    
    # Kursni olish
    course = get_course_by_id(context.user_data['course_id'])
    
    # Kurs sanalarini o'rnatish
    result = set_course_dates(
        context.user_data['course_id'],
        context.user_data['start_date'],
        end_date
    )
    
    if result:
        await update.message.reply_text(
            f"'{course['name']}' kursi uchun sanalar muvaffaqiyatli o'rnatildi:\n\n"
            f"Boshlanish: {context.user_data['start_date']}\n"
            f"Tugash: {end_date}"
        )
    else:
        await update.message.reply_text("Sanalar o'rnatilmadi. Kurs topilmadi.")
    
    # Kurs tafsilotlarini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("🔙 Kurs tafsilotlariga qaytish", callback_data=f"course_details_{context.user_data['course_id']}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("Sanalarni o'rnatish yakunlandi.", reply_markup=reply_markup)
    
    # User data'ni tozalash
    context.user_data.clear()
    
    return ConversationHandler.END

async def set_max_students_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurs uchun maksimal o'quvchilar sonini o'rnatish uchun so'rash"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return ConversationHandler.END
    
    # Kurs ID'sini olish
    course_id = int(query.data.split("_")[3])
    
    # Kursni olish
    course = get_course_by_id(course_id)
    
    if not course:
        await query.edit_message_text("Kurs topilmadi.")
        return ConversationHandler.END
    
    # Kurs ID'sini saqlash
    context.user_data['course_id'] = course_id
    
    await query.edit_message_text(
        f"'{course['name']}' kursi uchun maksimal o'quvchilar sonini kiriting:"
    )
    
    return COURSE_MAX_STUDENTS

async def set_max_students(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maksimal o'quvchilar sonini saqlash va o'rnatish"""
    try:
        max_students = int(update.message.text)
        
        # Kursni olish
        course = get_course_by_id(context.user_data['course_id'])
        
        # Maksimal o'quvchilar sonini o'rnatish
        result = set_course_max_students(
            context.user_data['course_id'],
            max_students
        )
        
        if result:
            await update.message.reply_text(
                f"'{course['name']}' kursi uchun maksimal o'quvchilar soni muvaffaqiyatli o'rnatildi: {max_students}"
            )
        else:
            await update.message.reply_text("Maksimal o'quvchilar soni o'rnatilmadi. Kurs topilmadi.")
        
        # Kurs tafsilotlarini qayta ko'rsatish
        keyboard = [
            [InlineKeyboardButton("🔙 Kurs tafsilotlariga qaytish", callback_data=f"course_details_{context.user_data['course_id']}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Maksimal o'quvchilar sonini o'rnatish yakunlandi.", reply_markup=reply_markup)
        
        # User data'ni tozalash
        context.user_data.clear()
        
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text(
            "Noto'g'ri format. Iltimos, raqam kiriting.\n\n"
            "Masalan: 20"
        )
        return COURSE_MAX_STUDENTS