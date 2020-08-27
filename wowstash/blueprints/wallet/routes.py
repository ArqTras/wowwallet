from flask import request, render_template, session, redirect, url_for, current_app
from flask_login import login_required, current_user
from wowstash.blueprints.wallet import wallet_bp
from wowstash.library.jsonrpc import wallet, daemon
from wowstash.factory import login_manager
from wowstash.models import User


@wallet_bp.route("/wallet/dashboard")
@login_required
def dashboard():
    user = User.query.get(current_user.id)
    wallet_height = wallet.height()['height']
    daemon_height = daemon.height()['height']
    subaddress = wallet.get_address(0, user.subaddress_index)['addresses'][0]['address']
    return render_template(
        "account/dashboard.html",
        wallet_height=wallet_height,
        daemon=daemon_height,
        subaddress=subaddress
    )
