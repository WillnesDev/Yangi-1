import os
import pandas as pd
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config.settings import DATA_DIR
from utils.db_manager import get_all_students, get_all_teachers, get_all_courses, get_course_students, get_course_by_id
from utils.permissions import check_admin

async def excel_reports_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Excel hisobotlar panelini ko'rsatish"""
    query = update.callback_query

    if query:
        await query.answer()
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("👨‍🎓 O'quvchilar ro'yxati", callback_data="excel_students")
            ],
            [
                InlineKeyboardButton("👨‍🏫 O'qituvchilar ro'yxati", callback_data="excel_teachers")
            ],
            [
                InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="excel_courses")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("Excel hisobotlar:", reply_markup=reply_markup)
    else:
        user_id = update.effective_user.id
        
        if not await check_admin(user_id):
            await update.message.reply_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("👨‍🎓 O'quvchilar ro'yxati", callback_data="excel_students")
            ],
            [
                InlineKeyboardButton("👨‍🏫 O'qituvchilar ro'yxati", callback_data="excel_teachers")
            ],
            [
                InlineKeyboardButton("📚 Kurslar ro'yxati", callback_data="excel_courses")
            ],
            [
                InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_admin")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("Excel hisobotlar:", reply_markup=reply_markup)

def generate_students_excel():
    """O'quvchilar ro'yxatini Excel formatida yaratish"""
    # Ma'lumotlarni olish
    students = get_all_students()

    # Ma'lumotlarni DataFrame'ga o'tkazish
    df = pd.DataFrame(students)

    # Fayl nomi
    filename = f"students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(DATA_DIR, filename)

    # Excel faylini yaratish
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(filepath, index=False)

    return filepath

def generate_teachers_excel():
    """O'qituvchilar ro'yxatini Excel formatida yaratish"""
    # Ma'lumotlarni olish
    teachers = get_all_teachers()

    # Ma'lumotlarni DataFrame'ga o'tkazish
    df = pd.DataFrame(teachers)

    # Fayl nomi
    filename = f"teachers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(DATA_DIR, filename)

    # Excel faylini yaratish
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(filepath, index=False)

    return filepath

def generate_courses_excel():
    """Kurslar ro'yxatini Excel formatida yaratish"""
    # Ma'lumotlarni olish
    courses = get_all_courses()

    # Ma'lumotlarni DataFrame'ga o'tkazish
    df = pd.DataFrame(courses)

    # Fayl nomi
    filename = f"courses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(DATA_DIR, filename)

    # Excel faylini yaratish
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(filepath, index=False)

    return filepath

def generate_course_students_excel(course_id, course_name):
    """Kursga yozilgan o'quvchilar ro'yxatini Excel formatida yaratish"""
    # Ma'lumotlarni olish
    students = get_course_students(course_id)

    # Ma'lumotlarni DataFrame'ga o'tkazish
    df = pd.DataFrame(students)

    # Fayl nomi
    filename = f"{course_name}_students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(DATA_DIR, filename)

    # Excel faylini yaratish
    os.makedirs(DATA_DIR, exist_ok=True)
    df.to_excel(filepath, index=False)

    return filepath

async def send_students_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'quvchilar ro'yxatini Excel formatida yuborish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return

    try:
        # Excel faylini yaratish
        filepath = generate_students_excel()
        
        # Faylni yuborish
        with open(filepath, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename=os.path.basename(filepath),
                caption="O'quvchilar ro'yxati"
            )
        
        # Excel hisobotlar paneliga qaytish
        keyboard = [[InlineKeyboardButton("🔙 Excel hisobotlar paneliga qaytish", callback_data="excel_reports")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "O'quvchilar ro'yxati yuborildi.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"Xatolik yuz berdi: {str(e)}")

async def send_teachers_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """O'qituvchilar ro'yxatini Excel formatida yuborish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return

    try:
        # Excel faylini yaratish
        filepath = generate_teachers_excel()
        
        # Faylni yuborish
        with open(filepath, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename=os.path.basename(filepath),
                caption="O'qituvchilar ro'yxati"
            )
        
        # Excel hisobotlar paneliga qaytish
        keyboard = [[InlineKeyboardButton("🔙 Excel hisobotlar paneliga qaytish", callback_data="excel_reports")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "O'qituvchilar ro'yxati yuborildi.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"Xatolik yuz berdi: {str(e)}")

async def send_courses_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kurslar ro'yxatini Excel formatida yuborish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return

    try:
        # Excel faylini yaratish
        filepath = generate_courses_excel()
        
        # Faylni yuborish
        with open(filepath, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename=os.path.basename(filepath),
                caption="Kurslar ro'yxati"
            )
        
        # Excel hisobotlar paneliga qaytish
        keyboard = [[InlineKeyboardButton("🔙 Excel hisobotlar paneliga qaytish", callback_data="excel_reports")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "Kurslar ro'yxati yuborildi.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"Xatolik yuz berdi: {str(e)}")

async def send_course_students_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kursga yozilgan o'quvchilar ro'yxatini Excel formatida yuborish"""
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id

    if not await check_admin(user_id):
        await query.edit_message_text("Sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return

    try:
        data = query.data
        course_id = int(data.split("_")[3])
        
        # Kurs nomini olish
        course = get_course_by_id(course_id)
        if not course:
            await query.edit_message_text("Kurs topilmadi.")
            return
        
        # Excel faylini yaratish
        filepath = generate_course_students_excel(course_id, course['name'])
        
        # Faylni yuborish
        with open(filepath, 'rb') as file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=file,
                filename=os.path.basename(filepath),
                caption=f"{course['name']} kursiga yozilgan o'quvchilar ro'yxati"
            )
        
        # Kurs ma'lumotlariga qaytish
        keyboard = [[InlineKeyboardButton("🔙 Kurs ma'lumotlariga qaytish", callback_data=f"course_details_{course_id}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "O'quvchilar ro'yxati yuborildi.",
            reply_markup=reply_markup
        )
    except Exception as e:
        await query.edit_message_text(f"Xatolik yuz berdi: {str(e)}")