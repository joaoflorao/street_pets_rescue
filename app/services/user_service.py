class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def get_user_types_list(self):
        return self.user_repository.get_user_types_list()

    def check_user_exists(self, email):
        user = self.user_repository.get_by_email(email)
        return user

    def create_user(self, *args):
        return self.user_repository.create_user(*args)

    def get_animals_by_user(self, user_id):
        return self.user_repository.get_animals_by_user(user_id)

    def adopt_animal(self, user, animal):
        return self.user_repository.adopt_animal(user, animal)
