from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from flask_bcrypt import generate_password_hash, check_password_hash
from wowstash.factory import db


Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    password = db.Column(db.String(120))
    email = db.Column(db.String(50), unique=True, index=True)
    subaddress_index = db.Column(db.Integer)
    registered_on = db.Column(db.DateTime, server_default=func.now())

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
