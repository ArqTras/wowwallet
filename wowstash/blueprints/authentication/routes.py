from flask import request, render_template, session, redirect, url_for
from wowstash.blueprints.authentication import authentication_bp
from wowstash.forms import Register
from wowstash.models import User


@authentication_bp.route("/register", methods=["GET", "POST"])
def register():
    form = Register()
    if form.validate_on_submit():
        print(dir(User))
        # user = User.query
        user = User.objects.filter(email=form.email.data)
        print(user)
        return "ok"
    else:
        print(form)
    return render_template("authentication/register.html", form=form)

@authentication_bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("authentication/login.html")

@authentication_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
