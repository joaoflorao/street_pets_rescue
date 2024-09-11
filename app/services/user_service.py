class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def check_user_exists(self, email):
        user = self.user_repository.get_by_email(email)
        return user

    def create_user(self, *args):
        return self.user_repository.create_user(*args)
