from app.models.animal_location_history import AnimalLocationHistory
from datetime import datetime


class AnimalLocationHistoryRepository:
    def __init__(self, session):
        self.session = session

    def add_animal_location(self, animal_id, new_location, start_date, end_date):
        current_date = datetime.utcnow()

        last_animal_location = self.get_last_location(animal_id)
        if last_animal_location and last_animal_location.end_date is None:
            last_animal_location.end_date = current_date

        if not start_date:
            start_date = current_date

        new_animal_location = AnimalLocationHistory(
            animal_id=animal_id,
            location=new_location,
            start_date=start_date,
            end_date=end_date,
        )
        self.session.add(new_animal_location)
        self.session.commit()
        return new_animal_location

    def get_last_location(self, animal_id):
        last_animal_location = AnimalLocationHistory.query.filter_by(
            animal_id=animal_id
        ).order_by(
            AnimalLocationHistory.start_date.desc()
        ).first()
        return last_animal_location

    def get_location_history(self, animal_id):
        animal_location_history = AnimalLocationHistory.query.filter_by(
            animal_id=animal_id
        ).order_by(
            AnimalLocationHistory.start_date.asc()
        ).all()
        return animal_location_history
