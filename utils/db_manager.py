import os
import json
from datetime import datetime

from config.settings import DATA_DIR

# Ma'lumotlar fayllari
STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')
TEACHERS_FILE = os.path.join(DATA_DIR, 'teachers.json')
ENROLLMENTS_FILE = os.path.join(DATA_DIR, 'enrollments.json')
ADMINS_FILE = os.path.join(DATA_DIR, 'admins.json')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')

def initialize_database():
    """Ma'lumotlar fayllarini yaratish"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Fayllarni yaratish
    if not os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(COURSES_FILE):
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(TEACHERS_FILE):
        with open(TEACHERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(ENROLLMENTS_FILE):
        with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(ADMINS_FILE):
        from config.settings import ADMIN_ID
        with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
            json.dump([ADMIN_ID], f, ensure_ascii=False, indent=4)
    
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

# Kurslar uchun funksiyalar
def add_course(name, description, duration, price):
    """Yangi kurs qo'shish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # Yangi kurs ID'sini aniqlash
    course_id = 1
    if courses:
        course_id = max(course['id'] for course in courses) + 1
    
    # Yangi kurs
    new_course = {
        'id': course_id,
        'name': name,
        'description': description,
        'duration': duration,
        'price': price,
        'teacher_id': None,
        'start_date': None,
        'end_date': None,
        'max_students': 0,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    courses.append(new_course)
    
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)
    
    return course_id

def get_all_courses():
    """Barcha kurslarni olish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    return courses

def get_course_by_id(course_id):
    """ID bo'yicha kursni olish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    for course in courses:
        if course['id'] == course_id:
            return course
    
    return None

def update_course(course_id, name, description, duration, price):
    """Kursni yangilash"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    for i, course in enumerate(courses):
        if course['id'] == course_id:
            courses[i]['name'] = name
            courses[i]['description'] = description
            courses[i]['duration'] = duration
            courses[i]['price'] = price
            
            with open(COURSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(courses, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def delete_course(course_id):
    """Kursni o'chirish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    # Kursni o'chirish
    courses = [course for course in courses if course['id'] != course_id]
    
    with open(COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, ensure_ascii=False, indent=4)
    
    # Kursga yozilishlarni o'chirish
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    enrollments = [enrollment for enrollment in enrollments if enrollment['course_id'] != course_id]
    
    with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(enrollments, f, ensure_ascii=False, indent=4)
    
    return True

# O'qituvchilar uchun funksiyalar
def add_teacher(name, subject, experience, contact):
    """Yangi o'qituvchi qo'shish"""
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    # Yangi o'qituvchi ID'sini aniqlash
    teacher_id = 1
    if teachers:
        teacher_id = max(teacher['id'] for teacher in teachers) + 1
    
    # Yangi o'qituvchi
    new_teacher = {
        'id': teacher_id,
        'name': name,
        'subject': subject,
        'experience': experience,
        'contact': contact
    }
    
    teachers.append(new_teacher)
    
    with open(TEACHERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(teachers, f, ensure_ascii=False, indent=4)
    
    return teacher_id

def get_all_teachers():
    """Barcha o'qituvchilarni olish"""
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    return teachers

def get_teacher_by_id(teacher_id):
    """ID bo'yicha o'qituvchini olish"""
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    for teacher in teachers:
        if teacher['id'] == teacher_id:
            return teacher
    
    return None

def update_teacher(teacher_id, name, subject, experience, contact):
    """O'qituvchini yangilash"""
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    for i, teacher in enumerate(teachers):
        if teacher['id'] == teacher_id:
            teachers[i]['name'] = name
            teachers[i]['subject'] = subject
            teachers[i]['experience'] = experience
            teachers[i]['contact'] = contact
            
            with open(TEACHERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(teachers, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def delete_teacher(teacher_id):
    """O'qituvchini o'chirish"""
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    # O'qituvchini o'chirish
    teachers = [teacher for teacher in teachers if teacher['id'] != teacher_id]
    
    with open(TEACHERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(teachers, f, ensure_ascii=False, indent=4)
    
    return True

# O'quvchilar uchun funksiyalar
def add_student(telegram_id, name, phone):
    """Yangi o'quvchi qo'shish"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    # O'quvchi allaqachon mavjudligini tekshirish
    for student in students:
        if student['telegram_id'] == telegram_id:
            return None
    
    # Yangi o'quvchi
    new_student = {
        'id': len(students) + 1,
        'telegram_id': telegram_id,
        'name': name,
        'phone': phone,
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    students.append(new_student)
    
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    
    return new_student['id']

def get_all_students():
    """Barcha o'quvchilarni olish"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    return students

def get_student_by_telegram_id(telegram_id):
    """Telegram ID bo'yicha o'quvchini olish"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    for student in students:
        if student['telegram_id'] == telegram_id:
            return student
    
    return None

def update_student(telegram_id, name, phone):
    """O'quvchini yangilash"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    for i, student in enumerate(students):
        if student['telegram_id'] == telegram_id:
            students[i]['name'] = name
            students[i]['phone'] = phone
            
            with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(students, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def delete_student(telegram_id):
    """O'quvchini o'chirish"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    # O'quvchini o'chirish
    students = [student for student in students if student['telegram_id'] != telegram_id]
    
    with open(STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, ensure_ascii=False, indent=4)
    
    # O'quvchining kursga yozilishlarini o'chirish
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    enrollments = [enrollment for enrollment in enrollments if enrollment['user_id'] != telegram_id]
    
    with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(enrollments, f, ensure_ascii=False, indent=4)
    
    return True

# Kursga yozilish uchun funksiyalar
def enroll_student(user_id, course_id, course_name):
    """O'quvchini kursga yozish"""
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    # O'quvchi allaqachon kursga yozilganligini tekshirish
    for enrollment in enrollments:
        if enrollment['user_id'] == user_id and enrollment['course_id'] == course_id:
            return False
    
    # Yangi yozilish
    new_enrollment = {
        'id': len(enrollments) + 1,
        'user_id': user_id,
        'course_id': course_id,
        'course_name': course_name,
        'enrollment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    enrollments.append(new_enrollment)
    
    with open(ENROLLMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(enrollments, f, ensure_ascii=False, indent=4)
    
    return True

def get_student_enrollments(user_id):
    """O'quvchi yozilgan kurslarni olish"""
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    return [enrollment for enrollment in enrollments if enrollment['user_id'] == user_id]

def get_all_enrollments():
    """Barcha kursga yozilishlarni olish"""
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    return enrollments

# Adminlar uchun funksiyalar
def add_admin(telegram_id):
    """Yangi admin qo'shish"""
    with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
        admins = json.load(f)
    
    # Admin allaqachon mavjudligini tekshirish
    if telegram_id in admins:
        return False
    
    admins.append(telegram_id)
    
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(admins, f, ensure_ascii=False, indent=4)
    
    return True

def is_admin(telegram_id):
    """Foydalanuvchi admin ekanligini tekshirish"""
    with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
        admins = json.load(f)
    
    return telegram_id in admins

def get_all_admins():
    """Barcha adminlarni olish"""
    with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
        admins = json.load(f)
    
    return admins

def remove_admin(telegram_id):
    """Adminni o'chirish"""
    with open(ADMINS_FILE, 'r', encoding='utf-8') as f:
        admins = json.load(f)
    
    if telegram_id not in admins:
        return False
    
    admins.remove(telegram_id)
    
    with open(ADMINS_FILE, 'w', encoding='utf-8') as f:
        json.dump(admins, f, ensure_ascii=False, indent=4)
    
    return True

# Kurslar uchun qo'shimcha funksiyalar
def assign_teacher_to_course(course_id, teacher_id):
    """Kursga o'qituvchi tayinlash"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    for i, course in enumerate(courses):
        if course['id'] == course_id:
            courses[i]['teacher_id'] = teacher_id
            
            with open(COURSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(courses, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def set_course_dates(course_id, start_date, end_date):
    """Kurs boshlanish va tugash sanalarini o'rnatish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    for i, course in enumerate(courses):
        if course['id'] == course_id:
            courses[i]['start_date'] = start_date
            courses[i]['end_date'] = end_date
            
            with open(COURSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(courses, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def set_course_max_students(course_id, max_students):
    """Kurs uchun maksimal o'quvchilar sonini o'rnatish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    for i, course in enumerate(courses):
        if course['id'] == course_id:
            courses[i]['max_students'] = max_students
            
            with open(COURSES_FILE, 'w', encoding='utf-8') as f:
                json.dump(courses, f, ensure_ascii=False, indent=4)
            
            return True
    
    return False

def get_course_students(course_id):
    """Kursga yozilgan o'quvchilarni olish"""
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    course_enrollments = [enrollment for enrollment in enrollments if enrollment['course_id'] == course_id]
    
    course_students = []
    for enrollment in course_enrollments:
        for student in students:
            if student['telegram_id'] == enrollment['user_id']:
                student_info = student.copy()
                student_info['enrollment_date'] = enrollment['enrollment_date']
                course_students.append(student_info)
                break
    
    return course_students

def get_course_teacher(course_id):
    """Kurs o'qituvchisini olish"""
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    course = None
    for c in courses:
        if c['id'] == course_id:
            course = c
            break
    
    if not course or not course['teacher_id']:
        return None
    
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    for teacher in teachers:
        if teacher['id'] == course['teacher_id']:
            return teacher
    
    return None

# Statistika uchun funksiyalar
def get_stats():
    """Statistika ma'lumotlarini olish"""
    with open(STUDENTS_FILE, 'r', encoding='utf-8') as f:
        students = json.load(f)
    
    with open(COURSES_FILE, 'r', encoding='utf-8') as f:
        courses = json.load(f)
    
    with open(TEACHERS_FILE, 'r', encoding='utf-8') as f:
        teachers = json.load(f)
    
    with open(ENROLLMENTS_FILE, 'r', encoding='utf-8') as f:
        enrollments = json.load(f)
    
    stats = {
        'students_count': len(students),
        'courses_count': len(courses),
        'teachers_count': len(teachers),
        'enrollments_count': len(enrollments)
    }
    
    return stats

# Davomat uchun funksiyalar
def add_attendance(student_id, course_id, date, status):
    """Davomat qo'shish"""
    with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
        attendance = json.load(f)
    
    # Yangi davomat
    new_attendance = {
        'id': len(attendance) + 1,
        'student_id': student_id,
        'course_id': course_id,
        'date': date,
        'status': status
    }
    
    attendance.append(new_attendance)
    
    with open(ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(attendance, f, ensure_ascii=False, indent=4)
    
    return new_attendance['id']

def get_student_attendance(student_id, course_id=None):
    """O'quvchi davomatini olish"""
    with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
        attendance = json.load(f)
    
    if course_id:
        return [a for a in attendance if a['student_id'] == student_id and a['course_id'] == course_id]
    else:
        return [a for a in attendance if a['student_id'] == student_id]

def get_course_attendance(course_id, date=None):
    """Kurs davomatini olish"""
    with open(ATTENDANCE_FILE, 'r', encoding='utf-8') as f:
        attendance = json.load(f)
    
    if date:
        return [a for a in attendance if a['course_id'] == course_id and a['date'] == date]
    else:
        return [a for a in attendance if a['course_id'] == course_id]