from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    add_users = StringField('Напишите id пользователей через пробел которых вы хотите добавить',
                            validators=[DataRequired()])
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')


class LessonForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')


