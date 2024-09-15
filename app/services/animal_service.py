class AnimalService:
    def __init__(self, animal_repository):
        self.animal_repository = animal_repository

    def register_animal(self, *args):
        return self.animal_repository.register_animal(*args)

    def get_status_list(self):
        return self.animal_repository.get_status_list()

    def get_animals_list(self):
        return self.animal_repository.get_animals_list()
