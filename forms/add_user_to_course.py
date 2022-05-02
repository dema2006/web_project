from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class InviteForm(FlaskForm):
    title = StringField('Введите код приглашения', validators=[DataRequired()])
    submit = SubmitField('Применить')