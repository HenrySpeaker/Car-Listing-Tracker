from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, NumberRange

notification_choices = [n for n in range(7, 29, 7)]


class OneOf:
    def __init__(self, other_field: str = "", message: str = ""):
        self.other_field = other_field
        if not message:
            message = "Exactly one field is required."
        self.message = message

    def __call__(self, form, field):
        field_data = field.data


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=50)])
    email = EmailField("Email", validators=[
                       InputRequired(), Length(min=1, max=100)])
    password = StringField("Password", validators=[
                           InputRequired(), Length(min=8, max=200)])
    notification_frequency = IntegerField(
        "Notification frequency", validators=[InputRequired(), NumberRange(min=1, max=30)])


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=50)])
    email = EmailField("Email", validators=[
                       InputRequired(), Length(min=1, max=100)])
    password = StringField("Password", validators=[
                           InputRequired(), Length(min=8, max=200)])
