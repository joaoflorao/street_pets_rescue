from app.services import db
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
from .event_type import EventType


class AnimalHistory(db.Model):
    __tablename__ = 'animal_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    action_type = db.Column(SqlEnum(EventType), nullable=False)
    description = db.Column(db.String, nullable=False)
    event_date = db.Column(db.Date)

    def __init__(self, animal_id, action_type, description, event_date):
        self.animal_id = animal_id
        self.action_type = EventType(action_type)
        self.description = description
        self.event_date = event_date

    animals_reference = db.relationship("Animal", back_populates="location_history")
