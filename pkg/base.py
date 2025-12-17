import sqlite3

db_name = "base.db"

class InitBase:
    def __init__(self):
        try:
            self.con = sqlite3.connect(db_name, check_same_thread=False)
            self.cur = self.con.cursor()
            print("База подключена")
            self.create_table()  
        except Exception as e:
            print(f"Ошибка подключения: {e}")

    def create_table(self):
        try:
            self.cur.execute(""" \
            CREATE TABLE IF NOT EXISTS user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            role TEXT,
            status TEXT,
            password TEXT NOT NULL); \
            """)

            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            subject TEXT,
            description TEXT,
            author TEXT,
            data DATE,
            status TEXT);
            """)

            self.con.commit()
            print("Таблица создана")
        except Exception as e:
            print(f"Ошибка создания таблицы: {e}")

#_____Запросы к таблице Users________#
    
    def users_add(self, username, email, phone, role, status, password):
        try:
            self.cur.execute(""" 
            INSERT INTO user(
            username, 
            email,
            phone,
            role,
            status,
            password)
            VALUES (?,?,?,?,?,?)""",
            (username, email, phone, role ,status, password))
            self.con.commit()
            print(f"Пользователь {username} добавлен")
            return True
        except sqlite3.IntegrityError:
            print("Ошибка: email уже существует")
            return False
        except Exception as e:
            print(f"Ошибка добавления: {e}")
            return False

    def select_users(self):
        """Получить всех пользователей"""
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT id, username, email, phone, role, status, password FROM user")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Ошибка выборки: {e}")
            return []

    def check_user(self, username, password):
        """Проверить пользователя по логину и паролю"""
        try:
            cursor = self.con.cursor()
            cursor.execute("""
                SELECT id, username, email, phone 
                FROM user 
                WHERE username = ? AND password = ?
            """, (username, password))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                # Преобразуем кортеж в словарь
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'phone': user[3]
                }
            return None
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return None

    def check_user_by_email(self, email, password):
        """Проверить пользователя по email и паролю"""
        try:
            cursor = self.con.cursor()
            cursor.execute("""
                SELECT id, username, email, phone 
                FROM user 
                WHERE email = ? AND password = ?
            """, (email, password))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'phone': user[3]
                }
            return None
        except Exception as e:
            print(f"Ошибка проверки: {e}")
            return None

    def get_user_by_email(self, email):
        """Получить пользователя по email"""
        try:
            cursor = self.con.cursor()
            cursor.execute("""
                SELECT id, username, email, phone, password 
                FROM user 
                WHERE email = ?
            """, (email,))
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'phone': user[3],
                    'password': user[4]
                }
            return None
        except Exception as e:
            print(f"Ошибка получения: {e}")
            return None
        
    def delet_user_by_id(self, user_id):
        try:
            self.cur.execute("""DELETE FROM user WHERE id=?""",(user_id,))
        except Exception as e:
            print(e)

#________Запросы к таблице Tickets_____________
   
    def tickets_add(self, category, subject, description, author, date_str, status):
        try:
            self.cur.execute(""" \
            INSERT INTO tickets(
            category,
            subject,
            description,
            author,
            data,
            status)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (category,subject, description, author, date_str, status))
            self.con.commit()
            print(f"Тикет {id} добавлен")
            return True
        except Exception as e:
            print(f"Ошибка добавления: {e}")
            return False

    def select_tickets(self):
        """Получить Тикеты"""
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT id, category, subject, description, author, data, status FROM tickets")
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            print(f"Ошибка выборки: {e}")
            return []

    def update_tickets_progress(self, ticket_id, status):
        cursor = self.con.cursor()
        cursor.execute("UPDATE tickets SET status = ? WHERE id = ?", (status, ticket_id))
        self.con.commit()

    def close(self):
        """Закрыть соединение с БД"""
        if self.con:
            self.con.close()
            print("Соединение закрыто")