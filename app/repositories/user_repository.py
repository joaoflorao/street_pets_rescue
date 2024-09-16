from app.models.user import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        return self.session.query(User).filter_by(email=email).first()

    def create_user(self, *args):
        new_user = User(*args)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def adopt_animal(self, user, animal):
        user.animals.append(animal)
        self.session.commit()
        return user.animals

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(int(user_id))
