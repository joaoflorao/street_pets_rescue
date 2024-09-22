from app.services import db
from flask_login import UserMixin
from datetime import datetime
import enum
from sqlalchemy import Enum as SqlEnum


class AnimalStatus(enum.Enum):
    available = "Disponivel"
    adopted = "Adotado"
    lost = "Perdido"
    deceased = "Falecido"


class Animal(db.Model):
    __tablename__ = "animal"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    animal_species = db.Column(db.String)
    animal_sex = db.Column(db.String)
    animal_size = db.Column(db.String)
    animal_adapt = db.Column(db.Boolean)
    characteristics = db.Column(db.String)
    chronic_illness = db.Column(db.String)
    continuous_treatments = db.Column(db.String)
    special_needs = db.Column(db.String)
    status = db.Column(SqlEnum(AnimalStatus))
    rescue_date = db.Column(db.Date)
    registration_date = db.Column(db.Date)

    def __init__(
        self,
        name,
        animal_species,
        animal_sex,
        animal_size,
        animal_adapt,
        characteristics,
        chronic_illness,
        continuous_treatments,
        special_needs,
        status,
        rescue_date
    ):
        self.name = name
        self.animal_species = animal_species
        self.animal_sex = animal_sex
        self.animal_size = animal_size
        self.animal_adapt = animal_adapt
        self.characteristics = characteristics
        self.chronic_illness = chronic_illness
        self.continuous_treatments = continuous_treatments
        self.special_needs = special_needs
        self.status = AnimalStatus(status)
        self.rescue_date = rescue_date
        self.registration_date = datetime.now()

    users = db.relationship("User", secondary="user_animal", back_populates="animals")
