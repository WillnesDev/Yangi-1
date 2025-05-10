from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from utils.permissions import check_admin
from utils.db_manager import get_stats, get_all_students, get_all_courses, get_all_teachers, get_all_enrollments

async def show_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Statistika panelini ko'rsatish"""
    query = update.callback_query
    
    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        # Statistika ma'lumotlarini olish
        stats = get_stats()
        
        message = "📊 Statistika paneli:\n\n"
        message += f"👨‍🎓 O'quvchilar soni: {stats['students_count']}\n"
        message += f"📚 Kurslar soni: {stats['courses_count']}\n"
        message += f"👨‍🏫 O'qituvchilar soni: {stats['teachers_count']}\n"
        message += f"📝 Kursga yozilishlar soni: {stats['enrollments_count']}\n"
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Batafsil statistika", callback_data="detailed_stats")
            ],
            [
                InlineKeyboardButton("📅 Oylik hisobot", callback_data="monthly_report")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(message, reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        # Statistika ma'lumotlarini olish
        stats = get_stats()
        
        message = "📊 Statistika paneli:\n\n"
        message += f"👨‍🎓 O'quvchilar soni: {stats['students_count']}\n"
        message += f"📚 Kurslar soni: {stats['courses_count']}\n"
        message += f"👨‍🏫 O'qituvchilar soni: {stats['teachers_count']}\n"
        message += f"📝 Kursga yozilishlar soni: {stats['enrollments_count']}\n"
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Batafsil statistika", callback_data="detailed_stats")
            ],
            [
                InlineKeyboardButton("📅 Oylik hisobot", callback_data="monthly_report")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(message, reply_markup=reply_markup)

async def show_detailed_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Batafsil statistikani ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Statistika ma'lumotlarini olish
    students = get_all_students()
    courses = get_all_courses()
    teachers = get_all_teachers()
    enrollments = get_all_enrollments()
    
    message = "📊 Batafsil statistika:\n\n"
    
    # O'quvchilar statistikasi
    message += "👨‍🎓 O'quvchilar:\n"
    message += f"Umumiy soni: {len(students)}\n"
    
    # Kurslar statistikasi
    message += "\n📚 Kurslar:\n"
    message += f"Umumiy soni: {len(courses)}\n"
    
    # O'qituvchilar statistikasi
    message += "\n👨‍🏫 O'qituvchilar:\n"
    message += f"Umumiy soni: {len(teachers)}\n"
    
    # Kursga yozilishlar statistikasi
    message += "\n📝 Kursga yozilishlar:\n"
    message += f"Umumiy soni: {len(enrollments)}\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Orqaga", callback_data="show_dashboard")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)

async def generate_monthly_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Oylik hisobotni ko'rsatish"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return
    
    # Statistika ma'lumotlarini olish
    students = get_all_students()
    courses = get_all_courses()
    teachers = get_all_teachers()
    enrollments = get_all_enrollments()
    
    message = "📅 Oylik hisobot:\n\n"
    
    # O'quvchilar statistikasi
    message += "👨‍🎓 O'quvchilar:\n"
    message += f"Umumiy soni: {len(students)}\n"
    
    # Kurslar statistikasi
    message += "\n📚 Kurslar:\n"
    message += f"Umumiy soni: {len(courses)}\n"
    
    # O'qituvchilar statistikasi
    message += "\n👨‍🏫 O'qituvchilar:\n"
    message += f"Umumiy soni: {len(teachers)}\n"
    
    # Kursga yozilishlar statistikasi
    message += "\n📝 Kursga yozilishlar:\n"
    message += f"Umumiy soni: {len(enrollments)}\n"
    
    keyboard = [
        [InlineKeyboardButton("🔙 Orqaga", callback_data="show_dashboard")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(message, reply_markup=reply_markup)