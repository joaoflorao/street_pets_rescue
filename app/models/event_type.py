import enum


class EventType(enum.Enum):
    register = "Cadastro"
    health = "Saúde"
    location = "Localização"
    vaccine = "Vacinação"
    status = "Alteração de status"
    rescued = "Resgate"
    adoption_monitoring = "Acompanhamento de adoção"
    return_of_adopted_animal = "Devolução de animal adotado"
