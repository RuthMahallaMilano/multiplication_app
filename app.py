from consts import app, db, DB_PATH

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user

from model import Exercise, User

from os import path
import random
from werkzeug.security import check_password_hash, generate_password_hash


def create_database() -> None:
    if not path.exists(DB_PATH):
        db.create_all()


def create_exercises_table() -> None:
    if len(Exercise.query.all()) == 0:
        exercises = []
        for i in range(1, 11):
            for j in range(1, 11):
                num1 = i
                num2 = j
                exercise = f"{num1} X {num2}"
                ans = num1 * num2
                exercises.append((exercise, ans))
        random.shuffle(exercises)
        for exercise, ans in exercises:
            ex_line = Exercise(ex=exercise, answer=ans, score=1)
            db.session.add(ex_line)
        db.session.commit()
        

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


create_database()
create_exercises_table()


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # if user solved all exercises:
        if session["current_question"] == 100:      
            return render_template("success.j2", user=current_user)
        current_ex = Exercise.query.get(session["current_question"])
        entered_answer = request.form.get('answer')
        if not entered_answer:
            flash("Please enter an answer", "error")
        elif entered_answer != str(current_ex.answer):
            flash("The answer is incorrect. Try again.", category="error")
        else:
            flash('Correct answer!', category='success')
            user_id = session["user_id"]
            user = User.query.filter_by(id=user_id).first()
            user.exercises.append(current_ex)
            db.session.add(user)
            db.session.commit()
            session["current_question"] += 1
    # if it's the first time:
    elif not User.query.filter_by(id=session["user_id"]).first().exercises:
        session["current_question"] = 1
    current_ex = Exercise.query.get(session["current_question"])
    solved, score = get_solved_exercises_and_score()
    return render_template("home.j2", question=current_ex.ex, user=current_user, solved=solved, score=score)


def get_solved_exercises_and_score():
    solved_exercises = User.query.filter_by(id=session["user_id"]).first().exercises
    solved = ((exercise.ex, exercise.answer) for exercise in solved_exercises)
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
                if User.query.filter_by(id=session["user_id"]).first().exercises:
                    session["current_question"] = User.query.filter_by(id=session["user_id"]).first().exercises[-1].id + 1
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
