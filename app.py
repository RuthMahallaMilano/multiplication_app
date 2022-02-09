from consts import app, db, DB_PATH

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user

from model import Exercise, User

from os import path
import random
from werkzeug.security import check_password_hash, generate_password_hash


def create_database() -> None:
    if not path.exists(DB_PATH):
        db.create_all()
        print('Created Database!')


def create_exercises_table() -> None:
    print(len(Exercise.query.all()))
    if len(Exercise.query.all()) == 0:
        for i in range(1, 11):
            for j in range(1, 11):
                num1 = i
                num2 = j
                exercise = f"{num1} X {num2}"
                ans = num1 * num2
                ex_line = Exercise(ex=exercise, answer=ans, score=1)
                db.session.add(ex_line)
        db.session.commit()


def create_login_manager(app: Flask) -> None:
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


def get_random_exercises_dict() -> dict:
    exercises = Exercise.query.all()
    random.shuffle(exercises)
    shuffled_exercises = [{'ex': ex.ex, 'answer': ex.answer} for ex in exercises]
    d = dict(enumerate(shuffled_exercises, 1))
    return {str(key): value for key, value in d.items()}


create_database()
create_exercises_table()
create_login_manager(app)
exercises_dict = get_random_exercises_dict()
# print(exercises_dict)

@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # print("current_question" in session)
    if request.method == 'POST':
        entered_answer = request.form.get('answer')
        # print("current_question" in session)
        # print(session["current_question"])
        # print(entered_answer)
        # print(exercises_dict[session["current_question"]]["answer"])
        if not entered_answer:
            flash("Please enter an answer", "error")
        elif entered_answer != str(exercises_dict[session["current_question"]]["answer"]):
            flash("The answer is incorrect. Try again.", category="error")
        else:
            flash('Correct answer!', category='success')
            solved_ex = Exercise.query.filter_by(ex=exercises_dict[session["current_question"]]["ex"]).first()
            user_id = session["user_id"]
            user = User.query.filter_by(id=user_id).first()
            user.exercises.append(solved_ex)
            db.session.add(user)
            db.session.commit()
            session["current_question"] = str(int(session["current_question"]) + 1)
    elif "current_question" not in session:
        score = get_solved_exercises_and_score()[1]
        session["current_question"] = str(score + 1)
    elif session["current_question"] not in exercises_dict:
        session.pop("current_question")
        return render_template("success.j2", user=current_user)
    solved, score = get_solved_exercises_and_score()
    return render_template("home.j2", question=exercises_dict[session["current_question"]]["ex"], user=current_user, solved=solved, score=score)


def get_solved_exercises_and_score():
    solved_exercises = User.query.filter_by(id=session["user_id"]).first().exercises
    solved = [exercise.ex for exercise in solved_exercises]
    score = sum([exercise.score for exercise in solved_exercises])
    return solved, score


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        user = User.query.filter_by(name=nickname).first()
        if user:
            if check_password_hash(user.password, password):
                session["user_id"] = user.id
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Nickname does not exist.', category='error')
    return render_template("login.j2", user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("current_question")
    return redirect(url_for('login'))


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(name=nickname).first()
        if user:
            flash('User already exists.', category='error')
        elif len(nickname) < 2:
            flash('Nickname must be at least 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 4:
            flash('Password must be at least 4 characters', category='error')
        else:
            new_user = User(name=nickname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.id
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('home'))    
    return render_template("sign_up.j2", user=current_user)


if __name__ == '__main__':
    app.run()
