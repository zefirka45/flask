from main import *
from datetime import datetime
from pkg import base

db = base.InitBase()

def add_tickets():
    current_datetime = datetime.now()
    if request.method == 'POST':
        category = request.form.get('category')
        subject = request.form.get('subject') 
        description = request.form.get('description')
        author = session['username']
        data = current_datetime
        status = "new"
        try:
            db.tickets_add(category,subject,description,author,data,status)
            print("Тикет Создан")
            return redirect("/create-ticket")
        except Exception as e:
            print(e)

def read_tickets():
    rows = db.select_tickets()  
    tickets = []
    for row in rows:
        ticket = {
            'id': row[0],
            'category': row[1],
            'subject': row[2],
            'description': row[3],
            'author': row[4],
            'data': row[5],      
            'status': row[6],
            'done': False
        }
        tickets.append(ticket)
    return tickets

def update_status():
    try:
        # --- 1. Проверка JSON ---
        if not request.is_json:
            return jsonify({'error': 'Требуется JSON'}), 400

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Пустой JSON'}), 400

        ticket_id = data.get('id')
        status = data.get('status')

        if not ticket_id or not status:
            return jsonify({'error': 'Нужны id и status'}), 400

        # --- 2. Преобразование и валидация ---
        try:
            ticket_id = int(ticket_id)
        except (ValueError, TypeError):
            return jsonify({'error': 'ID должен быть числом'}), 400

        if status not in ('in_progress', 'closed'):
            return jsonify({'error': 'Неверный статус'}), 400

        # --- 3. Обновление ---
        db.update_tickets_progress(ticket_id, status)  # ← Может выбросить исключение

        return jsonify({'success': True}), 200

    except Exception as e:
        print("❗ ОШИБКА В UPDATE_STATUS:", repr(e))
        return jsonify({'error': 'Серверная ошибка'}), 500

    except Exception as e:
        # Эта ветка ОБЯЗАНА вернуть ответ
        print(f"Неожиданная ошибка в update_status: {e}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500