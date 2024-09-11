from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from . import Base
import enum
from datetime import datetime


class AnimalStatus(enum.Enum):
    available = "Disponivel"
    adopted = "Adotado"
    lost = "Perdido"
    deceased = "Falecido"


class Animal(Base):
    __tablename__ = "animal"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    animal_type = Column(String)
    characteristics = Column(String)
    health_needs = Column(String)
    continuous_treatments = Column(String)
    special_needs = Column(String)
    status = Column(Enum(AnimalStatus))
    rescue_date = Column(Date)
    registration_date = Column(Date)

    def __init__(
        self,
        name,
        animal_type,
        characteristics,
        health_needs,
        continuous_treatments,
        special_needs,
        status,
        rescue_date,
    ):
        self.name = name
        self.animal_type = animal_type
        self.characteristics = characteristics
        self.health_needs = health_needs
        self.continuous_treatments = continuous_treatments
        self.special_needs = special_needs
        self.status = AnimalStatus(status)
        self.rescue_date = rescue_date
        self.registration_date = datetime.now()

    users = relationship("User", secondary="user_animal", back_populates="animals")
