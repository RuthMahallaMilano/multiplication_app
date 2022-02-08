from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


load_dotenv()

SECRETKEY = os.getenv("KEY")

DB_PATH = 'sqlite:///C:\\Users\\israe\\homework\\week15\\multiplication_app\\multiplication.db'


def init_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRETKEY
    return app


def init_db_connection(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    db = SQLAlchemy(flask_app)
    return db


app = init_app()
db = init_db_connection(app)
