import os
from flask import Flask
from .repositories.user_repository import UserRepository
from .repositories.animal_repository import AnimalRepository
from .repositories.animal_location_repository import AnimalLocationHistoryRepository
from .services.user_service import UserService
from .services.animal_service import AnimalService
from .services.animal_location_service import AnimalLocationHistoryService
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
animal_location_repository = AnimalLocationHistoryRepository(db.session)
animal_location_service = AnimalLocationHistoryService(animal_location_repository)

@login_manager.user_loader
def load_user(user_id):
    return UserRepository.get_user_by_id(user_id)


# Rotas
from .controllers.user_controller import bp as user_bp
from .controllers.animal_controller import bp as animal_bp
from .controllers.animal_location_controller import bp as animal_location_bp

app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(animal_bp, url_prefix="/animal")

app.register_blueprint(animal_location_bp, url_prefix="/animal_location_history")

from . import views
