from flask import request, render_template, session, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from wowstash.blueprints.authentication import authentication_bp
from wowstash.forms import Register, Login
from wowstash.models import User
from wowstash.library.jsonrpc import wallet
from wowstash.factory import db, bcrypt


@authentication_bp.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if current_user.is_authenticated:
        flash('Already registered and authenticated.')
        return redirect(url_for('wallet.dashboard'))

    if form.validate_on_submit():
        # Check if Wownero wallet is available
        if wallet.connected is False:
            flash('Wallet RPC interface is unavailable at this time. Try again later.')
            return redirect(url_for('authentication.register'))

        # Check if email already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('This email is already registered.')
            return redirect(url_for('authentication.login'))

        # Create new subaddress
        subaddress = wallet.new_address(label=form.email.data)

        # Save new user
        user = User(
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode('utf8'),
            subaddress_index=subaddress[0]
        )
        db.session.add(user)
        db.session.commit()

        # Login user and redirect to wallet page
        login_user(user)
        return redirect(url_for('wallet.dashboard'))

    return render_template("authentication/register.html", form=form)

@authentication_bp.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for('authentication.login'))

        # Check if password is correct
        password_matches = bcrypt.check_password_hash(
            user.password,
            form.password.data
        )
        if not password_matches:
            flash('Invalid username or password.')
            return redirect(url_for('authentication.login'))

        # Login user and redirect to wallet page
        login_user(user)
        return redirect(url_for('wallet.dashboard'))

    return render_template("authentication/login.html", form=form)

@authentication_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('meta.index'))
