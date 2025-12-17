from main import *
from pkg import base
db = base.InitBase()

def check():
    if request.method == 'POST':
        email = request.form.get('username')
        password = request.form.get('password')
        user = db.check_user_by_email(email, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Неверный email или пароль')
    
    return render_template('login.html')
