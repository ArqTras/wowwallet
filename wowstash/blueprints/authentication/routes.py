from flask import request, render_template, session, redirect, url_for
from wallet.blueprints.authentication import authentication_bp
from wallet.library.daemon import daemon
from wallet.library.wallet import wallet
from monero.seed import Seed
from binascii import hexlify
from datetime import datetime
from os import urandom

@authentication_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get('seed'):
            try:
                seed = Seed(str(request.form['seed']))

                session['seed'] = seed.phrase
                session['start_time'] = datetime.utcnow()
                session['public_address'] = seed.public_address()
                session['private_spend_key'] = seed.secret_spend_key()
                session['public_spend_key'] = seed.public_spend_key()
                session['private_view_key'] = seed.secret_view_key()
                session['public_view_key'] = seed.public_view_key()
                session['wallet_password'] = hexlify(urandom(64))
                if request.form.get('persistence'):
                    session['wallet_persistence'] = "Enabled"
                else:
                    session['wallet_persistence'] = "Disabled"
                return redirect(url_for('account.overview'))
            except AssertionError:
                error = "Invalid seed checksum"
            except Exception as e:
                error = "Invalid seed {0}".format(e)

        else:
            error = "Must provide a seed"

    return render_template("login.html", error=error)

@authentication_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))
