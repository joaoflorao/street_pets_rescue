from app.models.animal import Animal
from app.models.animal_status import AnimalStatus
from app.repositories.utils import handle_query_error


class AnimalRepository:
    def __init__(self, session):
        self.session = session

    def register_animal(self, *args):
        try:
            new_animal = Animal(*args)
            self.session.add(new_animal)
            self.session.commit()
            return new_animal
        except Exception as e:
            self.session.rollback()
            raise e

    def get_status_list(self):
        return AnimalStatus

    @handle_query_error
    def get_animals_list(self, status):
        animal_status = AnimalStatus(status)
        return self.session.query(Animal).filter_by(status=animal_status).all()

    @handle_query_error
    def get_animal_by_id(self, animal_id):
        return self.session.query(Animal).filter_by(id=animal_id).first()

    def update_animal_status(self, animal_id, status):
        try:
            animal = self.get_animal_by_id(animal_id)
            animal.status = AnimalStatus(status)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
