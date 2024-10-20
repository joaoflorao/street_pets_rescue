class AnimalService:
    def __init__(self, animal_repository):
        self.animal_repository = animal_repository

    def register_animal(self, *args):
        return self.animal_repository.register_animal(*args)

    def get_status_list(self):
        return self.animal_repository.get_status_list()

    def get_animals_by_user_preference(self, filters, animal_status):
        animals_with_score = []
        animals_list = self.animal_repository.get_animals_list(animal_status)
        for animal in animals_list:
            animal_score = self.calc_animal_score(animal, filters)
            animals_with_score.append((animal, animal_score))

        animals_with_score.sort(key=lambda x: x[1], reverse=True)
        animals_list = [animal for animal, score in animals_with_score]

        return animals_list

    def get_animal_by_id(self, animal_id):
        return self.animal_repository.get_animal_by_id(animal_id)

    def update_animal_status(self, animal_id, status):
        return self.animal_repository.update_animal_status(animal_id, status)

    def calc_animal_score(self, animal, filters):
        score = 0

        if animal.animal_species == filters.get("animal_species"):
            score += 20

        if animal.animal_size == filters.get("animal_size"):
            score += 10

        if animal.animal_sex == filters.get("animal_sex"):
            score += 5

        if animal.animal_adapt:
            score += 5

        # Necessidades especiais e tratamentos continuos
        tutor_accepts_special_needs = filters.get("accept_animal_with_continuous_treatment")
        has_special_needs = bool(animal.special_needs or animal.continuous_treatments)
        if has_special_needs:
            if tutor_accepts_special_needs:
                score += 10
        else:
            if not tutor_accepts_special_needs:
                score += 10
            else:
                score += 5

        # Doencas cronicas
        tutor_accepts_chronic_illness = filters.get("accept_animal_with_chronic_illness")
        has_chronic_illness = bool(animal.chronic_illness)
        if has_chronic_illness:
            if tutor_accepts_chronic_illness:
                score += 10
            else:
                score += 5

        # Tempo do tutor com o animal
        tutor_time_availability = filters.get("tutor_time_availability")
        if (has_special_needs or has_chronic_illness) and tutor_time_availability:
            score += 5

        return score
