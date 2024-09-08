from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .animal import Animal
from .user import User
