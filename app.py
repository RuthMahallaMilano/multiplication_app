from consts import app, db, DB_PATH
from flask import session, render_template, request, flash, redirect, url_for
from os import path
from model import Exercise, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random


def create_database():
    if not path.exists(DB_PATH):
        db.create_all()
        print('Created Database!')


def create_exercises_table():
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


def create_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


create_database()
create_exercises_table()
create_login_manager(app)


#TODO  ליצור עוד כדף בית שמופיעים בו כל היוזרים והתוצאות שלהם????


def get_random_exercises_dict():
    exercises = Exercise.query.all()
    random.shuffle(exercises)
    shuffled_exercises = [{'ex': ex.ex, 'answer': ex.answer} for ex in exercises]
    d = dict(enumerate(shuffled_exercises, 1))
    # print(d)
    return {str(key): value for key, value in d.items()}


exercises_dict = get_random_exercises_dict()
# print(exercises_dict)


@app.route('/', methods=['GET', 'POST'])  
@login_required
def home():

    if request.method == 'POST':
        entered_answer = request.form.get('answer')
        if not entered_answer:
            flash("Please enter an answer", "error")
        elif entered_answer != str(exercises_dict[session["current_question"]]["answer"]):
            flash("The answer is incorrect. Try again", "error")
        else:
            flash('Correct answer!', category='success')
            solved_ex = Exercise.query.filter_by(ex=exercises_dict[session["current_question"]]["ex"]).first()
            user_id = session["user_id"]
            user = User.query.filter_by(id=user_id).first()
            user.exercises.append(solved_ex)
            db.session.add(user)
            db.session.commit()
            session["current_question"] = str(int(session["current_question"]) + 1)
            
    if "current_question" not in session:
        session["current_question"] = "1"

    elif session["current_question"] not in exercises_dict:   # not sure it works
        return render_template("success.html", user=current_user)
    
    solved_exercises = User.query.filter_by(id=session["user_id"]).first().exercises
    solved = [exercise.ex for exercise in solved_exercises]
    score = sum([exercise.score for exercise in solved_exercises])

    return render_template("home.html", question=exercises_dict[session["current_question"]]["ex"], user=current_user, solved=solved, score=score)
       

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        user = User.query.filter_by(name=nickname).first()
        session["user_id"] = user.id
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Nickname does not exist.', category='error')
        
    return render_template("login.html", user=current_user)


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

            login_user(new_user)
            flash('Account created!', category='success')
            return redirect(url_for('home'))

    return render_template("sign_up.html", user=current_user)


app.run(debug=True)