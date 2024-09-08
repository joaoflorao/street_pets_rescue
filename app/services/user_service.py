class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def login_user(self, email, password):
        login_is_valid = [False, False]
        user = self.user_repository.get_by_email(email)
        if user:
            login_is_valid = [
                user is not None,
                user.check_password(user.password, password),
            ]

        return login_is_valid

    def check_user_exists(self, email):
        user = self.user_repository.get_by_email(email)
        return user is not None

    def create_user(self, *args):
        return self.user_repository.create_user(*args)
