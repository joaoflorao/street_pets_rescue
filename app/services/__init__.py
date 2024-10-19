from .user_service import UserService
from .animal_service import AnimalService
from .animal_history_service import AnimalHistoryService

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
