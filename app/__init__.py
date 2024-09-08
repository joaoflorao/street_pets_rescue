import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import Base
from .repositories.user_repository import UserRepository
from .services.user_service import UserService

app = Flask(__name__)

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Cria as tabelas se elas não existirem
with app.app_context():
    Base.metadata.create_all(db.engine)

user_repository = UserRepository(db.session)
user_service = UserService(user_repository)

# Rotas
from .controllers.user_controller import bp as user_bp

app.register_blueprint(user_bp, url_prefix="/user")

from . import views
