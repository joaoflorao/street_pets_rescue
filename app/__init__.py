import os
from flask import Flask
from .repositories.user_repository import UserRepository
from .repositories.animal_repository import AnimalRepository
from .repositories.animal_history_repository import AnimalHistoryRepository
from .services.user_service import UserService
from .services.animal_service import AnimalService
from .services.animal_history_service import AnimalHistoryService
from .services import login_manager, db

app = Flask(__name__)

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager.init_app(app)

# Cria as tabelas se elas não existirem
with app.app_context():
    db.create_all()

# Repositories
user_repository = UserRepository(db.session)
user_service = UserService(user_repository)
animal_repository = AnimalRepository(db.session)
animal_service = AnimalService(animal_repository)
animal_history_repository = AnimalHistoryRepository(db.session)
animal_history_service = AnimalHistoryService(animal_history_repository)

@login_manager.user_loader
def load_user(user_id):
    return user_repository.get_user_by_id(user_id)


# Rotas
from .controllers.user_controller import bp as user_bp
from .controllers.animal_controller import bp as animal_bp
from .controllers.animal_history_controller import bp as animal_history_bp

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(animal_bp, url_prefix="/animal")

app.register_blueprint(animal_history_bp, url_prefix="/animal_history")

from . import views
