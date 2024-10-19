class AnimalHistoryService:
    def __init__(self, animal_history_repository):
        self.animal_history_repository = animal_history_repository

    def get_event_types(self):
        return self.animal_history_repository.get_event_types()

    def get_animal_history(self, animal_id):
        return self.animal_history_repository.get_animal_history(animal_id)

    def add_animal_event_history(self, *args):
        return self.animal_history_repository.add_animal_event_history(*args)
