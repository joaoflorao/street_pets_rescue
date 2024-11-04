from app.services import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
from .animal_status import AnimalStatus
import base64


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
    animal_image = db.Column(db.LargeBinary)

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
        rescue_date,
        animal_image
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
        self.animal_image = animal_image

    @property
    def image_base64(self):
        return base64.b64encode(self.animal_image).decode("utf-8")

    users = db.relationship("User", secondary="user_animal", back_populates="animals")
    location_history = db.relationship("AnimalHistory", back_populates="animals_reference",
                                       cascade="all, delete-orphan")
