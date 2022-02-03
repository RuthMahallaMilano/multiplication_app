# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy


# DB_PATH = 'sqlite:///C:\\Users\\israe\\homework\\week15\\multiplication_app\\multiplication.db'


# def init_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = '1234'

#     from .views import views
#     from .auth import auth
#     app.register_blueprint(views, url_prefix='/')
#     app.register_blueprint(auth, url_prefix='/')



#     return app


# def init_db_connection(flask_app):
#     flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
#     db = SQLAlchemy(flask_app)
#     return db