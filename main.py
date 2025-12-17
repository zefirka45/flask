from flask import Flask,render_template, redirect, request, flash, session, jsonify
from flask_restful import  Api
from flask_session import Session
from pkg import access, base, register,dashboard, admin
import json

db = base.InitBase()
db.create_table()

app = Flask(__name__)
api = Api(app)
app.config["SESSION_PERMANENT"] = False    
app.config["SESSION_TYPE"] = "filesystem" 
app.config['SECRET_KEY'] = 'fdgdfgdfggf786hfg6hfg6h7f'   
Session(app)

#Маршруты
@app.route("/")
def index():
    return render_template("index.html")

#Авторизация
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/check", methods=["GET", "POST"])
def check():
    return access.check()

#Регистрация 
@app.route("/register")
def registers():
    return render_template("register.html")

@app.route("/valid", methods=["GET", "POST"])
def valid():
    return register.validData()

#Панель администратора 
@app.route("/dashboard")
def dashboards():
    if not session.get("username"):
        return redirect("/login")
    return render_template("dashboard.html")

@app.route('/dashboard/tasks', methods=['GET'])
def get_tasks():
    return jsonify ({'tasks': dashboard.read_tickets()})

@app.route('/dashboard/update', methods=['POST'])
def update_ticket_status():
    return dashboard.update_status()

@app.route("/admin-panel")
def admin_panel():
    return render_template("admin.html")

@app.route("/admin-panel/read-users", methods=['GET'])
def read_users():
    return jsonify(admin.read_users())

@app.route("/admin-panel/delete-user/<int:user_id>", methods=['DELETE'])
def delete_users(user_id):
    return admin.delete_user(user_id)
    
#Создать заявку
@app.route("/create-ticket")
def create_ticket():
    return render_template("create-ticket.html")

@app.route("/create",methods=["GET", "POST"])
def create():
    return dashboard.add_tickets()

#Выход из панели
@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/login")

if __name__ == "__main__":
    app.run(
        debug=True,
        port=8005
    )
   
