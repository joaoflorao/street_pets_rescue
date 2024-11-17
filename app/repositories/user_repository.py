from app.models.user import User, user_animal_table
from app.models.animal import Animal
from .animal_history_repository import AnimalHistoryRepository
from app.models.animal_status import AnimalStatus
from app.models.user_type import UserType
from app.models.event_type import EventType
from app.repositories.utils import handle_query_error
from datetime import datetime


class UserRepository:
    def __init__(self, session):
        self.session = session

    @handle_query_error
    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def create_user(self, *args):
        try:
            new_user = User(*args)
            self.session.add(new_user)
            self.session.commit()
            return new_user
        except Exception as e:
            self.session.rollback()
            raise e

    def get_user_types_list(self):
        return UserType

    @handle_query_error
    def get_animals_by_user(self, user_id):
        animals = (
            self.session.query(Animal)
            .join(user_animal_table, Animal.id == user_animal_table.c.animal_id)
            .join(User, User.id == user_animal_table.c.user_id)
            .filter(User.id == user_id)
            .all()
        )
        return animals

    def adopt_animal(self, user, animal):
        try:
            animal_available = self.session.query(Animal).filter_by(id=animal.id, status='available').first()
            if not animal_available:
                raise Exception("Animal não está mais disponível para adoção.")

            user.animals.append(animal)
            animal_available.status = AnimalStatus("Adotado")

            event_description = "Animal adotado."
            AnimalHistoryRepository.add_animal_event_history(self, animal.id, EventType.status,
                                                             event_description, datetime.utcnow())
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    @staticmethod
    @handle_query_error
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))
