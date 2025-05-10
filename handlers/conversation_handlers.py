from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from services.admin_service import add_admin_start, add_admin_finish
from services.course_service import (
    add_course_start, add_course_name, add_course_description, add_course_duration, add_course_price,
    edit_course_start, edit_course_name, edit_course_description, edit_course_duration, edit_course_price,
    set_dates_start, set_start_date, set_end_date, set_max_students_start, set_max_students
)
from services.teacher_service import (
    add_teacher_start, add_teacher_name, add_teacher_subject, add_teacher_experience, add_teacher_contact,
    edit_teacher_start, edit_teacher_name, edit_teacher_subject, edit_teacher_experience, edit_teacher_contact
)
from services.student_service import (
    add_student_start, add_student_name, add_student_phone,
    edit_student_start, edit_student_name, edit_student_phone,
    register_start, register_name, register_phone
)
from services.notification_service import (
    notify_all_start, notify_all_finish, select_course, notify_course_finish,
    select_student, notify_student_finish
)

def register_conversation_handlers(application):
    """Barcha conversation handler'larini ro'yxatdan o'tkazish"""
    
    # Admin qo'shish
    add_admin_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_admin_start, pattern="^add_admin$")],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_admin_finish)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Kurs qo'shish
    add_course_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_course_start, pattern="^add_course$")],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_name)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_description)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_duration)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_course_price)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Kursni tahrirlash
    edit_course_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_course_start, pattern="^edit_course_\d+$")],
        states={
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_course_name)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_course_description)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_course_duration)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_course_price)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Kurs sanalarini o'rnatish
    set_dates_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(set_dates_start, pattern="^set_dates_\d+$")],
        states={
            8: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_start_date)],
            9: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_end_date)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Kurs uchun maksimal o'quvchilar sonini o'rnatish
    set_max_students_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(set_max_students_start, pattern="^set_max_students_\d+$")],
        states={
            10: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_max_students)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # O'qituvchi qo'shish
    add_teacher_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_teacher_start, pattern="^add_teacher$")],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_teacher_name)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_teacher_subject)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_teacher_experience)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_teacher_contact)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # O'qituvchini tahrirlash
    edit_teacher_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_teacher_start, pattern="^edit_teacher_\d+$")],
        states={
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_teacher_name)],
            5: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_teacher_subject)],
            6: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_teacher_experience)],
            7: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_teacher_contact)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # O'quvchi qo'shish
    add_student_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_student_start, pattern="^add_student$")],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_name)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_student_phone)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # O'quvchini tahrirlash
    edit_student_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_student_start, pattern="^edit_student_\d+$")],
        states={
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_student_name)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_student_phone)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Ro'yxatdan o'tish
    register_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(register_start, pattern="^register$"),
            CommandHandler("register", register_start)
        ],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_name)],
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, register_phone)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Barcha foydalanuvchilarga bildirishnoma yuborish
    notify_all_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(notify_all_start, pattern="^notify_all$")],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, notify_all_finish)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Kurs o'quvchilariga bildirishnoma yuborish
    notify_course_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_course, pattern="^select_course_\d+$")],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, notify_course_finish)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Bitta o'quvchiga bildirishnoma yuborish
    notify_student_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_student, pattern="^select_student_\d+$")],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, notify_student_finish)]
        },
        fallbacks=[CommandHandler("cancel", lambda update, context: ConversationHandler.END)]
    )
    
    # Handler'larni ro'yxatdan o'tkazish
    application.add_handler(add_admin_conv)
    application.add_handler(add_course_conv)
    application.add_handler(edit_course_conv)
    application.add_handler(set_dates_conv)
    application.add_handler(set_max_students_conv)
    application.add_handler(add_teacher_conv)
    application.add_handler(edit_teacher_conv)
    application.add_handler(add_student_conv)
    application.add_handler(edit_student_conv)
    application.add_handler(register_conv)
    application.add_handler(notify_all_conv)
    application.add_handler(notify_course_conv)
    application.add_handler(notify_student_conv)