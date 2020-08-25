from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = StringField('Email Address:', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "form-control", "type": "email"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})
