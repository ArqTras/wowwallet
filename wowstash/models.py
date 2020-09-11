from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from wowstash.factory import db


Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(50), unique=True, index=True)
    subaddress_index = db.Column(db.Integer)
    registered_on = db.Column(db.DateTime, server_default=func.now())
    funds_locked = db.Column(db.Boolean, default=False)

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

    def __repr__(self):
        return self.username


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column('tx_id', db.Integer, primary_key=True)
    from_user = db.Column(db.Integer, ForeignKey(User.id))
    sent = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(120))
    amount = db.Column(db.String(120))
    date = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return self.id
