from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_PATH = 'sqlite:///C:\\Users\\israe\\homework\\week15\\multiplication_app\\multiplication.db'


def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1234'
    # from views import views
    # from auth import auth
    # app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    return app


def init_db_connection(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    db = SQLAlchemy(flask_app)
    return db


app = init_app()
db = init_db_connection(app)










# @app.route('/')
# def home():
#     return render_template("home.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():

#     return render_template("login.html")


# @app.route('/logout')
# def logout():
#     return "logout"


# @app.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         nickname = request.form.get('Nickname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         if len(nickname) < 2:
#             flash('Nickname must be at least 2 characters', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match', category='error')
#         elif len(password1) < 4:
#             flash('Password must be at least 4 characters', category='error')
#         else:
#             flash('Account created', category='success')
#         # new_user = User()
#     return render_template("sign_up.html")


# # app.run(debug=True)