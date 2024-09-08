from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import Base
import bcrypt
from datetime import datetime


user_animal_table = Table(
    "user_animal",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("animal_id", Integer, ForeignKey("animal.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    password = Column(String)
    address = Column(String)
    registration_date = Column(Date)
    birth_date = Column(Date)

    animals = relationship("Animal", secondary="user_animal", back_populates="users")

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
