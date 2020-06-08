from .. import db, flask_bcrypt
import datetime
import jwt
from ..config import key


class Employee(db.model):
    """ User Model for storing user related details """
    __tablename__ = "employee"

    #id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    fname = db.Column(db.String(100), nullable=False )
    phone_no = db.Column(db.String(15), primary_key=True, unique=True)
    lname = db.Column(db.String(100), unique=True)
    isactive = db.Column(db.String(1))

    def __repr__(self):
        return "<Employee '{}'>".format(self.fname)
