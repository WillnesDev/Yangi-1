from utils.db_manager import is_admin

async def check_admin(user_id):
    """Foydalanuvchi admin ekanligini tekshirish"""
    return is_admin(user_id)