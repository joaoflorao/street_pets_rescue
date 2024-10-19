import enum


class EventType(enum.Enum):
    register = "Cadastro"
    health = "Saúde"
    location = "Localização"
    vaccine = "Vacinação"
    status = "Alteração de status"
