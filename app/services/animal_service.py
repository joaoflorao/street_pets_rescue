class AnimalService:
    def __init__(self, animal_repository):
        self.animal_repository = animal_repository

    def register_animal(self, *args):
        return self.animal_repository.register_animal(*args)

    def get_status_list(self):
        return self.animal_repository.get_status_list()

    def get_animals_list(self, status):
        return self.animal_repository.get_animals_list(status)

    def get_animal_by_id(self, animal_id):
        return self.animal_repository.get_animal_by_id(animal_id)

    def update_animal_status(self, animal_id, status):
        return self.animal_repository.update_animal_status(animal_id, status)
