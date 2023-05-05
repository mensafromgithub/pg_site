from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = name = StringField('Имя пользователя', validators=[DataRequired()])
    about = about = TextAreaField("Немного о себе")
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')