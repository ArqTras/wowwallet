from io import BytesIO
from base64 import b64encode
from qrcode import make as qrcode_make
from decimal import Decimal
from flask import request, render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from wowstash.blueprints.wallet import wallet_bp
from wowstash.library.jsonrpc import wallet, daemon
from wowstash.forms import Send
from wowstash.factory import login_manager, db
from wowstash.models import User, Transaction


@wallet_bp.route("/wallet/dashboard")
@login_required
def dashboard():
    all_transfers = list()
    send_form = Send()
    _address_qr = BytesIO()
    user = User.query.get(current_user.id)
    wallet_height = wallet.height()['height']
    subaddress = wallet.get_address(0, user.subaddress_index)
    balances = wallet.get_balance(0, user.subaddress_index)
    transfers = wallet.get_transfers(0, user.subaddress_index)
    txs_queued = Transaction.query.filter_by(from_user=user.id)
    for type in transfers:
        for tx in transfers[type]:
            all_transfers.append(tx)

    qr_uri = f'wownero:{subaddress}?tx_description="{current_user.email}"'
    address_qr = qrcode_make(qr_uri).save(_address_qr)
    qrcode = b64encode(_address_qr.getvalue()).decode()
    return render_template(
        "wallet/dashboard.html",
        wallet_height=wallet_height,
        subaddress=subaddress,
        balances=balances,
        all_transfers=all_transfers,
        qrcode=qrcode,
        send_form=send_form,
        txs_queued=txs_queued
    )

@wallet_bp.route("/wallet/send", methods=["GET", "POST"])
@login_required
def send():
    send_form = Send()
    redirect_url = url_for('wallet.dashboard') + "#send"
    if send_form.validate_on_submit():
        address = str(send_form.address.data)

        # Check if Wownero wallet is available
        if wallet.connected is False:
            flash('Wallet RPC interface is unavailable at this time. Try again later.')
            return redirect(redirect_url)

        # Check if user funds flag is locked
        if current_user.funds_locked:
            flash('You currently have transactions pending and transfers are locked. Try again later.')
            return redirect(redirect_url)

        # Quick n dirty check to see if address is WOW
        if len(address) not in [97, 108]:
            flash('Invalid Wownero address provided.')
            return redirect(redirect_url)

        # Make sure the amount provided is a number
        try:
            amount = Decimal(send_form.amount.data)
        except:
            flash('Invalid Wownero amount specified.')
            return redirect(redirect_url)

        # Lock user funds
        user = User.query.get(current_user.id)
        user.funds_locked = True
        db.session.commit()

        # Queue the transaction
        tx = Transaction(
            from_user=user.id,
            address=address,
            amount=amount,
        )
        db.session.add(tx)
        db.session.commit()

        # Redirect back
        flash('Successfully queued transfer.')
        return redirect(redirect_url)
    else:
        for field, errors in send_form.errors.items():
            flash(f'{send_form[field].label}: {", ".join(errors)}')
        return redirect(redirect_url)
