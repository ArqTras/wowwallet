from sqlalchemy import Column, Integer, DateTime, String
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
