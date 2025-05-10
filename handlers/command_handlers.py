from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from services.admin_service import admin_panel
from services.course_service import list_courses
from services.teacher_service import list_teachers
from services.student_service import list_students, my_courses
from services.excel_service import excel_reports_panel
from services.stats_service import show_dashboard
from services.notification_service import notification_panel

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot ishga tushganda ishlatiladigan buyruq"""
    user = update.effective_user
    await update.message.reply_html(
        f"Salom, {user.mention_html()}!\n\n"
        f"Kurslar boshqaruvi botiga xush kelibsiz. "
        f"Buyruqlar ro'yxatini ko'rish uchun /help buyrug'idan foydalaning."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yordam buyrug'i"""
    help_text = (
        "Buyruqlar ro'yxati:\n\n"
        "/start - Botni ishga tushirish\n"
        "/help - Yordam\n"
        "/admin - Admin panel\n"
        "/courses - Kurslar ro'yxati\n"
        "/teachers - O'qituvchilar ro'yxati\n"
        "/students - O'quvchilar ro'yxati\n"
        "/mycourses - Mening kurslarim\n"
        "/excel - Excel hisobotlar\n"
        "/dashboard - Statistika paneli\n"
        "/notify - Bildirishnomalar paneli\n"
    )
    await update.message.reply_text(help_text)

def register_command_handlers(application):
    """Barcha buyruq handler'larini ro'yxatdan o'tkazish"""
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CommandHandler("courses", list_courses))
    application.add_handler(CommandHandler("teachers", list_teachers))
    application.add_handler(CommandHandler("students", list_students))
    application.add_handler(CommandHandler("mycourses", my_courses))
    application.add_handler(CommandHandler("excel", excel_reports_panel))
    application.add_handler(CommandHandler("dashboard", show_dashboard))
    application.add_handler(CommandHandler("notify", notification_panel))