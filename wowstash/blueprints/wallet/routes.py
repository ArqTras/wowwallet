from flask import request, render_template, session, redirect, url_for, current_app
from flask_login import login_required, current_user
from wowstash.blueprints.wallet import wallet_bp
from wowstash.library.jsonrpc import wallet, daemon
from wowstash.factory import login_manager
from wowstash.models import User


@wallet_bp.route("/wallet/dashboard")
@login_required
def dashboard():
    all_transfers = list()
    user = User.query.get(current_user.id)
    wallet_height = wallet.height()['height']
    daemon_height = daemon.height()['height']
    subaddress = wallet.get_address(0, user.subaddress_index)
    balances = wallet.get_balance(0, user.subaddress_index)
    transfers = wallet.get_transfers(0, user.subaddress_index)
    for type in transfers:
        for tx in transfers[type]:
            all_transfers.append(tx)
    return render_template(
        "wallet/dashboard.html",
        wallet_height=wallet_height,
        daemon_height=daemon_height,
        subaddress=subaddress,
        balances=balances,
        all_transfers=all_transfers
    )
