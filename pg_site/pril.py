from flask import Flask, render_template, redirect, jsonify
from data import db_session, us_api
from data.users import User
from flask import make_response
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from data.login import LoginForm
from data.register import RegisterForm



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/download', methods=['GET'])
def download():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('download.html', title='Скачать версии')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=form.remember_me.data)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/place')
def place():
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(User.user_id).all()[0]
    return user.place


@app.route('/')
def table():
    return render_template('table.html', title='table')


@app.route('/us')
def us():
    return


def main():
    db_session.global_init("db/blogs.db")
    app.register_blueprint(us_api.blueprint)
    app.run(port=5000, host='127.0.0.1')


main()
