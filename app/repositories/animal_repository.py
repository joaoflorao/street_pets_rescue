from app.models.animal import Animal, AnimalStatus


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
