from consts import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    exercises = db.relationship("Exercise", secondary="user_exercises")


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    ex = db.Column(db.String, nullable=False)
    answer = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    

t_user_exercises = db.Table(
    "user_exercises",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("exercise_id", db.ForeignKey("exercises.id")),
)
