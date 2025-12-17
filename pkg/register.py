from main import *
from pkg import base
db = base.InitBase()
def validData():
    if request.method == 'POST':
        username = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']
        role = "user"
        status = "active"
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            try:    
                db.users_add(username, email, phone, role, status, password)
                print("Пользователь добавлен")
                return redirect("/login")
            except Exception as e:
                print(e)
                return render_template("register.html", error=str(e))
        else:
            print("Пароли разные")
            return render_template("register.html", error="Пароли не совпадают")
    else:
        print("Ошибка выполнения операции")
        return render_template("login.html")