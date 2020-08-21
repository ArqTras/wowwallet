from flask import request, render_template, session
from flask import redirect, url_for, current_app
from wallet.blueprints.account import account_bp
from wallet.library.daemon import daemon
from wallet.library.wallet import wallet

@account_bp.route("/account")
def overview():
    if session.get("public_address"):
        return render_template("account.html",
                               session_data=session,
                               h=daemon.get_height(),
                               wallet=wallet)
    else:
        return redirect(url_for("index"))

@account_bp.route("/account/wallet")
def connect_wallet():
    if session.get("public_address"):
        wallet.init(host=current_app.config['DAEMON_HOST'],
                    port=current_app.config['DAEMON_PORT'],
                    public_view_key=session['public_view_key'],
                    wallet_password=session['wallet_password'],
                    mnemonic_seed=session['seed'],
                    restore_height=daemon.get_height(),
                    path=current_app.config['BINARY_PATH'])
        return redirect(url_for("account.overview"))
    else:
        return redirect(url_for("index"))
