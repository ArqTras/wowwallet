from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = StringField('Email Address:', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "form-control", "type": "email"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})
    faq_reviewed = BooleanField('FAQ Reviewed:', validators=[DataRequired()], render_kw={"class": "form-control-span"})
    terms_reviewed = BooleanField('Terms Reviewed:', validators=[DataRequired()], render_kw={"class": "form-control-span"})
    privacy_reviewed = BooleanField('Privacy Policy Reviewed:', validators=[DataRequired()], render_kw={"class": "form-control-span"})

class Login(FlaskForm):
    email = StringField('Email Address:', validators=[DataRequired()], render_kw={"placeholder": "Email", "class": "form-control", "type": "email"})
    password = StringField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Password", "class": "form-control", "type": "password"})
