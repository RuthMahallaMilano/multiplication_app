from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


load_dotenv()

SECRETKEY = os.getenv("KEY")

DB_PATH = os.getenv("DATABASE_URL")


def init_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRETKEY
    return app


def init_db_connection(flask_app: Flask) -> SQLAlchemy:
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_PATH
    db = SQLAlchemy(flask_app)
    return db


app = init_app()
db = init_db_connection(app)
