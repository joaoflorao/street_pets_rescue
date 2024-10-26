from app.models.animal_history import AnimalHistory
from app.models.event_type import EventType
from datetime import datetime
from app.repositories.utils import handle_query_error


class AnimalHistoryRepository:
    def __init__(self, session):
        self.session = session

    def get_event_types(self):
        return EventType

    @handle_query_error
    def get_animal_history(self, animal_id):
        animal_history = AnimalHistory.query.filter_by(
            animal_id=animal_id
        ).order_by(
            AnimalHistory.event_date.asc()
        ).all()
        return animal_history

    def add_animal_event_history(self, *args):
        try:
            new_animal_event_history = AnimalHistory(*args)
            self.session.add(new_animal_event_history)
            self.session.commit()
            return new_animal_event_history
        except Exception as e:
            self.session.rollback()
            raise e
