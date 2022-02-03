from consts import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    # total_score = db.Column(db.Integer, nullable=False)
    exercises = db.relationship("Exercise", secondary="user_exercises")


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    ex = db.Column(db.String, nullable=False)
    answer = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # users = db.relationship("User", secondary="user_exercises")
    

t_user_exercises = db.Table(
    "user_exercises",
    db.Model.metadata,
    db.Column("user_id", db.ForeignKey("users.id")),
    db.Column("exercise_id", db.ForeignKey("exercises.id")),
)


# def create_exercises_db():
#     for i in range(1, 11):
#         for j in range(1, 11):
#             num1 = i
#             num2 = j
#             exercise = f"{num1} X {num2}"
#             ans = num1 * num2
#             ex_line = Exercise(ex=exercise, answer=ans, score=1)
#             db.session.add(ex_line)
#     db.session.commit()

# create_exercises_db()

# db.create_all()