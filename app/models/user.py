from app.services import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import bcrypt


user_animal_table = db.Table(
    "user_animal",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("animal_id", db.Integer, db.ForeignKey("animal.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone_number = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    address = db.Column(db.String)
    registration_date = db.Column(db.Date)
    birth_date = db.Column(db.Date)

    def __init__(self, name, email, password, birth_date):
        self.name = name
        self.email = email
        self.password = self.hash_password(password)
        self.registration_date = datetime.now()
        self.birth_date = birth_date

    def hash_password(self, password, enc_type="utf-8"):
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(enc_type), salt)
        return hashed.decode()

    def check_password(self, stored_password, entered_password, enc_type="utf-8"):
        stored_hash_bytes = stored_password.encode(enc_type)
        return bcrypt.checkpw(entered_password.encode(enc_type), stored_hash_bytes)

    animals = db.relationship("Animal", secondary="user_animal", back_populates="users")
