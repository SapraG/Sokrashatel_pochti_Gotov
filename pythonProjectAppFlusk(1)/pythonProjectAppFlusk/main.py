from flask import Flask, render_template, url_for, request, flash, session, redirect
import SQLRequest
from SQLRequest import *
import dbController
import sqlite3
import pyshorteners
import pyperclip
app = Flask(__name__)
app.config['SECRET_KEY'] = 'o1234k124gku124g12'


menu = ({'name': 'Авторизация', 'url': '/log'},
        {'name': 'Регистрация', 'url': '/reg'},
        {'name': 'Главная', 'url': '/'})


@app.route("/index", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        print(session.get('userLogged'))
        print(request.form['link'])
        print(request.form['type'])
        ski = pyshorteners.Shortener().tinyurl.short(request.form['link'])
        print(ski)
        kopy = ski
        pyperclip.copy(kopy)
    return render_template('index.html', menu=menu)


@app.route("/log", methods=["POST", "GET"])
def log():
    print(session.get('userLogged'))
    if session.get('userLogged') != None:
        return redirect(url_for('index', username=session['userLogged']))
    if request.method == 'POST':
        conn = sqlite3.connect('db.db')
        cur = conn.cursor()
        user = cur.execute('SELECT * FROM users WHERE login = ?', (request.form['login'],)).fetchone()
        pas = cur.execute('SELECT password FROM users')

        # работа с сессиями


        if request.method == 'POST' and request.form['login'] == user[1] and request.form['password'] == user[2]:
            session['userLogged'] = request.form['login']
            print(333)
            return redirect(url_for('index', username=session['userLogged']))
    return render_template('log.html', menu=menu)


@app.route("/reg", methods=["POST", "GET"])
def reg():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    if session.get('userLogged') != None:
        return redirect(url_for('index', username=session['userLogged']))
    if request.method == 'POST':
        if 'userLogged' in session:
            if request.form['password'] == request.form['password_confirmation']:
                name = request.form['login']
                ps = request.form['password_confirmation']
                cur.execute("""INSERT INTO users('login', 'password') VALUES(?,?)""", (name, ps))
                conn.commit()
                print(request.form['login'])
                print(request.form['password'])
                print(request.form['password_confirmation'])
                return redirect(url_for('log', username=session['userLogged']))
    return render_template('reg.html', menu=menu)




if __name__ == "__main__":
    app.run(debug=True)


