from main import *
from pkg import base
db = base.InitBase()

def read_users():
    rows = db.select_users() 
    users = []
    for row in rows:
        user = {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'phone': row[3],
            'role': row[4],
            'status':row[5]
        }
        users.append(user)
    return users

def delete_user(user_id):
    # 1. Проверка прав администратора (обязательно!)
    if not session.get("is_admin"):  # или любой ваш способ проверки
        return jsonify({'error': 'Доступ запрещён'}), 403

    # 2. Проверка существования
    if not db.select_users(user_id):
        return jsonify({'error': 'Пользователь не найден'}), 404

    # 3. Удаление
    try:
        db.delet_user_by_id(user_id)
        return jsonify({'success': True}), 200
    except Exception as e:
        print(f"Ошибка БД: {e}")
        return jsonify({'error': 'Ошибка при удалении'}), 500