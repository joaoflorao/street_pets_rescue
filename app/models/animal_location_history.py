from app.services import db
from datetime import datetime

class AnimalLocationHistory(db.Model):
    __tablename__ = 'animal_location_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)
    location = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)

    animals_reference = db.relationship('Animal', back_populates='location_history')
