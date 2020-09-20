from os import kill
from flask import request, render_template, session, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from secrets import token_urlsafe
from wowstash.blueprints.auth import auth_bp
from wowstash.forms import Register, Login
from wowstash.models import User
from wowstash.factory import db, bcrypt


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if current_user.is_authenticated:
        flash('Already registered and authenticated.')
        return redirect(url_for('wallet.dashboard'))

    if form.validate_on_submit():
        # Check if email already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('This email is already registered.')
            return redirect(url_for('auth.login'))

        # Save new user
        user = User(
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf8'),
            wallet_password=token_urlsafe(16),
        )
        db.session.add(user)
        db.session.commit()

        # Login user and redirect to wallet page
        login_user(user)
        return redirect(url_for('wallet.dashboard'))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if current_user.is_authenticated:
        flash('Already registered and authenticated.')
        return redirect(url_for('wallet.dashboard'))

    if form.validate_on_submit():
        # Check if user doesn't exist
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        # Check if password is correct
        password_matches = bcrypt.check_password_hash(
            user.password,
            form.password.data
        )
        if not password_matches:
            flash('Invalid username or password.')
            return redirect(url_for('auth.login'))

        # Login user and redirect to wallet page
        login_user(user)
        return redirect(url_for('wallet.dashboard'))

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        current_user.kill_wallet()
        current_user.clear_wallet_data()
    logout_user()
    return redirect(url_for('meta.index'))
