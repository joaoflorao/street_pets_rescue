class AnimalLocationHistoryService:
    def __init__(self, animal_location_repository):
        self.animal_location_repository = animal_location_repository

    def add_animal_location(self, animal_id, new_animal_location, start_date, end_date):
        return self.animal_location_repository.add_animal_location(
            animal_id, new_animal_location, start_date, end_date
        )

    def get_last_location(self, animal_id):
        return self.animal_location_repository.get_last_location(animal_id)

    def get_location_history(self, animal_id):
        return self.animal_location_repository.get_location_history(animal_id)
