from os import kill
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from wowstash.factory import db


Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(120))
    register_date = db.Column(db.DateTime, server_default=func.now())
    wallet_password = db.Column(db.String(120))
    wallet_created = db.Column(db.Boolean, default=False)
    wallet_connected = db.Column(db.Boolean, default=False)
    wallet_port = db.Column(db.Integer, nullable=True)
    wallet_pid = db.Column(db.Integer, nullable=True)
    wallet_connect_date = db.Column(db.DateTime, nullable=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.admin

    def get_id(self):
        return self.id

    def kill_wallet(self):
        try:
            kill(self.wallet_pid, 9)
        except Exception as e:
            print('could kill:', e)

    def clear_wallet_data(self):
        self.wallet_connected = False
        self.wallet_port = None
        self.wallet_pid = None
        self.wallet_connect_date = None
        db.session.commit()

    def __repr__(self):
        return self.email
