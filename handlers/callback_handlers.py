from telegram.ext import CallbackQueryHandler

from services.admin_service import (
    admin_panel, manage_users_panel, manage_admins_panel,
    add_admin_start, remove_admin_start, remove_admin_finish
)
from services.course_service import (
    manage_courses_panel, add_course_start, list_courses,
    edit_course_select, edit_course_start, delete_course_select,
    delete_course_confirm, delete_course_final, view_courses_user,
    enroll_course, course_details, assign_teacher_start, 
    select_teacher_finish, course_students_list, set_dates_start,
    set_max_students_start
)
from services.teacher_service import (
    manage_teachers_panel, add_teacher_start, list_teachers,
    edit_teacher_select, edit_teacher_start, delete_teacher_select,
    delete_teacher_confirm, delete_teacher_final
)
from services.student_service import (
    manage_students_panel, add_student_start, list_students,
    edit_student_select, edit_student_start, delete_student_select,
    delete_student_confirm, delete_student_final, my_courses,
    register_start
)
from services.excel_service import (
    excel_reports_panel, send_students_excel, send_teachers_excel, 
    send_courses_excel, send_course_students_excel
)
from services.stats_service import show_dashboard, show_detailed_stats, generate_monthly_report
from services.notification_service import (
    notification_panel, notify_all_start, notify_course_start,
    notify_student_start, select_course, select_student
)

async def button_callback(update, context):
    """Tugmalar bosilganda ishlaydigan funksiya"""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    # Admin panel
    if callback_data == "back_to_admin":
        await admin_panel(update, context)
    elif callback_data == "manage_courses":
        await manage_courses_panel(update, context)
    elif callback_data == "manage_teachers":
        await manage_teachers_panel(update, context)
    elif callback_data == "manage_students":
        await manage_students_panel(update, context)
    elif callback_data == "manage_users":
        await manage_users_panel(update, context)
    elif callback_data == "manage_admins":
        await manage_admins_panel(update, context)
    elif callback_data == "add_admin":
        return await add_admin_start(update, context)
    elif callback_data == "remove_admin":
        await remove_admin_start(update, context)
    elif callback_data.startswith("remove_admin_"):
        await remove_admin_finish(update, context)
    elif callback_data == "excel_reports":
        await excel_reports_panel(update, context)
    elif callback_data == "excel_students":
        await send_students_excel(update, context)
    elif callback_data == "excel_teachers":
        await send_teachers_excel(update, context)
    elif callback_data == "excel_courses":
        await send_courses_excel(update, context)
    elif callback_data.startswith("excel_course_students_"):
        await send_course_students_excel(update, context)
    
    # Dashboard va statistika
    elif callback_data == "show_dashboard":
        await show_dashboard(update, context)
    elif callback_data == "detailed_stats":
        await show_detailed_stats(update, context)
    elif callback_data == "monthly_report":
        await generate_monthly_report(update, context)
    
    # Bildirishnomalar
    elif callback_data == "notification_panel":
        await notification_panel(update, context)
    elif callback_data == "notify_all":
        return await notify_all_start(update, context)
    elif callback_data == "notify_course":
        await notify_course_start(update, context)
    elif callback_data == "notify_student":
        await notify_student_start(update, context)
    elif callback_data.startswith("select_course_"):
        return await select_course(update, context)
    elif callback_data.startswith("select_student_"):
        return await select_student(update, context)
    
    # Kurslar
    elif callback_data == "view_courses":
        await list_courses(update, context)
    elif callback_data == "view_courses_user":
        await view_courses_user(update, context)
    elif callback_data == "add_course":
        return await add_course_start(update, context)
    elif callback_data == "edit_course":
        await edit_course_select(update, context)
    elif callback_data.startswith("edit_course_"):
        return await edit_course_start(update, context)
    elif callback_data == "delete_course":
        await delete_course_select(update, context)
    elif callback_data.startswith("delete_course_"):
        await delete_course_confirm(update, context)
    elif callback_data.startswith("confirm_delete_course_") or callback_data == "cancel_delete_course":
        await delete_course_final(update, context)
    elif callback_data.startswith("course_details_"):
        await course_details(update, context)
    elif callback_data.startswith("assign_teacher_"):
        await assign_teacher_start(update, context)
    elif callback_data.startswith("select_teacher_"):
        await select_teacher_finish(update, context)
    elif callback_data.startswith("course_students_"):
        await course_students_list(update, context)
    elif callback_data.startswith("set_dates_"):
        return await set_dates_start(update, context)
    elif callback_data.startswith("set_max_students_"):
        return await set_max_students_start(update, context)
    
    # O'qituvchilar
    elif callback_data == "view_teachers":
        await list_teachers(update, context)
    elif callback_data == "add_teacher":
        return await add_teacher_start(update, context)
    elif callback_data == "edit_teacher":
        await edit_teacher_select(update, context)
    elif callback_data.startswith("edit_teacher_"):
        return await edit_teacher_start(update, context)
    elif callback_data == "delete_teacher":
        await delete_teacher_select(update, context)
    elif callback_data.startswith("delete_teacher_"):
        await delete_teacher_confirm(update, context)
    elif callback_data.startswith("confirm_delete_teacher_") or callback_data == "cancel_delete_teacher":
        await delete_teacher_final(update, context)
    
    # O'quvchilar
    elif callback_data == "view_students":
        await list_students(update, context)
    elif callback_data == "add_student":
        return await add_student_start(update, context)
    elif callback_data == "edit_student":
        await edit_student_select(update, context)
    elif callback_data.startswith("edit_student_"):
        return await edit_student_start(update, context)
    elif callback_data == "delete_student":
        await delete_student_select(update, context)
    elif callback_data.startswith("delete_student_"):
        await delete_student_confirm(update, context)
    elif callback_data.startswith("confirm_delete_student_") or callback_data == "cancel_delete_student":
        await delete_student_final(update, context)
    
    # Kursga yozilish
    elif callback_data.startswith("enroll_"):
        await enroll_course(update, context)
    elif callback_data == "my_courses":
        await my_courses(update, context)
    elif callback_data == "register":
        return await register_start(update, context)

def register_callback_handlers(application):
    """Barcha callback handler'larini ro'yxatdan o'tkazish"""
    application.add_handler(CallbackQueryHandler(button_callback))