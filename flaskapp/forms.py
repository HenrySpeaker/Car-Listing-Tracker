from typing import Any
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, IntegerField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange
from db.body_styles import body_styles

body_style_list = [body for body in body_styles.keys()]


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
    username = StringField("Username", validators=[Length(max=50)])
    email = EmailField("Email", validators=[Length(max=100)])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=8, max=200)])

    def validate(self, extra_validators=None):

        if not super().validate(extra_validators):
            return False

        check = (len(self.username.data) > 0) ^ (len(self.email.data) > 0)
        if not check:
            self.username.errors.append(
                "Only one of email or password can be submitted.")
            self.email.errors.append(
                "Only one of email or password can be submitted.")
        return check


class CriteriaForm(FlaskForm):
    min_year = IntegerField("Minimum car year", validators=[
                            NumberRange(min=1992, max=2023)])
    max_year = IntegerField("Maximum car year", validators=[
                            NumberRange(min=1992, max=2023)])

    min_price = IntegerField("Minimum car price", validators=[
                             InputRequired(), NumberRange(min=1, max=10000000)])
    max_price = IntegerField("Max car price", validators=[
                             InputRequired(), NumberRange(min=1, max=10000000)])

    max_mileage = IntegerField("Maximum car mileage (miles)", validators=[
                               InputRequired(), NumberRange(min=1, max=100000000)])

    search_distance = IntegerField("Maximum search radius from zip code", default=5, validators=[
                                   InputRequired(), NumberRange(min=1, max=50)])

    no_accidents = BooleanField("No accidents")

    single_owner = BooleanField("Single owner")

    body_style = SelectField(
        "Body style", choices=body_style_list, validators=[InputRequired()])

    zip_code = IntegerField("Search area zip code", validators=[
                            InputRequired(), NumberRange(min=1, max=99999)])

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators):
            return False

        if self.min_year.data > self.max_year.data:
            self.min_year.errors.append(
                "Minimum year must be less than maximum year")
            return False

        if self.min_price.data > self.max_price.data:
            self.min_price.errors.append(
                "Minimum car price must be less than maximum car price")

        return True
