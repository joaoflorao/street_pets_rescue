import enum


class AnimalStatus(enum.Enum):
    available = "Disponivel"
    adopted = "Adotado"
    lost = "Perdido"
    deceased = "Falecido"
