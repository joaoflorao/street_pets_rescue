from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_required, current_user
from app import animal_service, user_service, animal_history_service
from app.models.event_type import EventType
from app.models.animal_status import AnimalStatus
from datetime import datetime

bp = Blueprint("animal", __name__)


@bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    status_list = animal_service.get_status_list()
    if request.method == "GET":
        return render_template("register_animal.html", status_list=status_list)

    data = request.form
    animal_name = data.get("nAnimalName")
    animal_type = data.get("nAnimalSpecies")
    animal_sex = data.get("nAnimalSex")
    animal_size = data.get("nAnimalSize")
    animal_adapt = data.get("nAdaptOthersAnimals", type=int)
    characteristics = data.get("nCharacteristics")
    health_needs = data.get("nHealthNeeds")
    continuous_treatments = data.get("nContinuousTreatments")
    special_needs = data.get("nSpecialNeeds")
    animal_status = data.get("nAnimalStatus")
    rescue_date = data.get("nRescueDate")
    animal_image = request.files["nAnimalImage"]

    new_animal = animal_service.register_animal(
        animal_name, animal_type, animal_sex, animal_size, bool(animal_adapt),
        characteristics, health_needs, continuous_treatments,
        special_needs, animal_status, rescue_date, animal_image.read()
    )
    animal_id = new_animal.id
    session['animal_id'] = animal_id

    register_status = "Animal cadastrado"
    rescue_status = "Animal resgatado"

    animal_history_service.add_animal_event_history(animal_id, EventType.register.value,
                                                    register_status, datetime.utcnow())
    animal_history_service.add_animal_event_history(animal_id, EventType.rescued.value,
                                                    rescue_status, rescue_date)

    flash("Animal cadastrado com sucesso!", "success")
    return redirect(url_for("animal.animals_list"))


@bp.route("/list", methods=["GET", "POST"])
@login_required
def animals_list():
    data = request.form
    status_list = animal_service.get_status_list()

    animal_status = data.get("nAnimalStatus", type=str, default=AnimalStatus.available.value)
    if request.method == "GET":
        custom_filter = session.get("user_preferences_filter")

        animals_list = animal_service.get_animals_by_user_preference(custom_filter, animal_status)
        return render_template("list_animal.html", animals_list=animals_list, status_list=status_list)

    animal_species = data.get("nSpecies")
    animal_size = data.get("nSize")
    animal_sex = data.get("nSex")
    accept_animal_with_continuous_treatment = data.get("nTreatment", type=int)
    accept_animal_with_chronic_illness = data.get("nChronicIllness", type=int)
    tutor_owns_animals = data.get("nHaveAnimals", type=int)
    tutor_has_time_availability = data.get("nTimeAvailability", type=int)

    user_preferences_filter = {
        "animal_species": animal_species,
        "animal_size": animal_size,
        "animal_sex": animal_sex,
        "tutor_time_availability": bool(tutor_has_time_availability),
        "tutor_owns_animals": bool(tutor_owns_animals),
        "accept_animal_with_chronic_illness": bool(accept_animal_with_chronic_illness),
        "accept_animal_with_continuous_treatment": bool(accept_animal_with_continuous_treatment)
    }
    session['user_preferences_filter'] = user_preferences_filter

    animals_list = animal_service.get_animals_by_user_preference(user_preferences_filter, animal_status)
    return render_template("list_animal.html", animals_list=animals_list, status_list=status_list)


@bp.route("/detail", methods=["GET", "POST"])
@login_required
def animal_detail():
    data = request.form

    animal_id = data.get("nAnimalId", type=int)
    if not animal_id:
        animal_id = int(session['animal_id'])

    animal_info = animal_service.get_animal_by_id(animal_id)
    if not animal_info:
        flash("Animal não encontrado", "warning")
        return redirect(url_for("animal.animals_list"))

    session['animal_id'] = animal_id
    return render_template("detail_animal.html", animal=animal_info)


@bp.route("/adopt", methods=["POST"])
@login_required
def adopt_animal():
    animal_id = int(session['animal_id'])

    user_filter = session.get("user_preferences_filter")
    animal = animal_service.get_animal_by_id(animal_id)
    if animal.status.value != "Disponivel":
        message = f"O animal não está disponível para adoção ou já foi adotado por outra pessoa!"
        flash(message, "warning")
        return render_template("detail_animal.html", animal=animal)

    user_animals_list = user_service.get_animals_by_user(current_user.id)
    tutor_owns_animals = user_filter.get("tutor_owns_animals")
    if not animal.animal_adapt and (user_animals_list or tutor_owns_animals):
        message = f"Infelizmente {animal.name} não se adapta com animais, e você já possui animais!"
        flash(message, "warning")
        return render_template("detail_animal.html", animal=animal)

    tutor_has_time_availability = user_filter.get("tutor_time_availability")
    if not tutor_has_time_availability and animal.continuous_treatments:
        message = f"Esse animal exige cuidados constantes e você não possui tempo livre!"
        flash(message, "warning")
        return render_template("detail_animal.html", animal=animal)

    new_animal_status = "Adotado"
    animal = animal_service.update_animal_status(animal_id, new_animal_status)

    event_description = "Animal adotado."
    animal_history_service.add_animal_event_history(animal_id, EventType.status,
                                                    event_description, datetime.utcnow())
    user_service.adopt_animal(current_user, animal)

    flash(f"Parabéns! Você adotou o {animal.name}!", "success")
    return redirect(url_for("animal.animal_detail"))
