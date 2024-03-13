from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrar')


class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    content = TextAreaField('Conteúdo', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('>')


class CommentForm(FlaskForm):
    content = StringField('Comentário', validators=[DataRequired(), Length(max=150)])
    submit = SubmitField('Enviar')