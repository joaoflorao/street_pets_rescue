from app.models.animal import Animal
from app.models.animal_status import AnimalStatus


class AnimalRepository:
    def __init__(self, session):
        self.session = session

    def register_animal(self, *args):
        new_animal = Animal(*args)
        self.session.add(new_animal)
        self.session.commit()
        return new_animal

    def get_status_list(self):
        return AnimalStatus

    def get_animals_list(self, status):
        return self.session.query(Animal).filter_by(status=status).all()

    def get_animal_by_id(self, animal_id):
        return self.session.query(Animal).filter_by(id=animal_id).first()

    def update_animal_status(self, animal_id, status):
        animal = self.get_animal_by_id(animal_id)
        animal.status = AnimalStatus(status)
        self.session.commit()
        return animal
