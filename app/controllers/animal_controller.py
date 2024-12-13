from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_required, current_user
from app import animal_service, user_service, animal_history_service
from app.models.event_type import EventType
from app.models.animal_status import AnimalStatus
from datetime import datetime
from app import app

bp = Blueprint("animal", __name__)


@bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    try:
        # Block users without permission
        if not (current_user.is_admin() or current_user.is_protector()):
            flash("Você não tem permissão para cadastrar animais!", "warning")
            return redirect(url_for("animal.animals_list"))

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

        # Animal register
        new_animal = animal_service.register_animal(
            animal_name, animal_type, animal_sex, animal_size, bool(animal_adapt),
            characteristics, health_needs, continuous_treatments,
            special_needs, animal_status, rescue_date, animal_image.read()
        )
        animal_id = new_animal.id
        session['animal_id'] = animal_id

        register_status = "Animal cadastrado"
        rescue_status = "Animal resgatado"

        # Add animal events history
        animal_history_service.add_animal_event_history(animal_id, EventType.register.value,
                                                        register_status, datetime.utcnow())
        animal_history_service.add_animal_event_history(animal_id, EventType.rescued.value,
                                                        rescue_status, rescue_date)

        flash("Animal cadastrado com sucesso!", "success")
        return redirect(url_for("animal.animals_list"))
    except Exception as e:
        message_error = "Erro ao cadastrar o animal!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return redirect(url_for("animal.animals_list"))


@bp.route("/list", methods=["GET", "POST"])
@login_required
def animals_list():
    try:
        session.page_title = "Vitrine de animais"
        data = request.form
        status_list = animal_service.get_status_list()

        animal_status = data.get("nAnimalStatus", type=str, default=AnimalStatus.available.value)
        if request.method == "GET":
            custom_filter = session.get("user_preferences_filter")

            animals_list = animal_service.get_animals_by_user_preference(custom_filter, animal_status)
            qtde_animals = len(animals_list)
            return render_template("list_animal.html", animals_list=animals_list,
                                   status_list=status_list, qtde_animals=qtde_animals)

        # Get user preferences
        animal_species = data.get("nSpecies")
        animal_size = data.get("nSize")
        animal_sex = data.get("nSex")
        accept_animal_with_continuous_treatment = data.get("nTreatment", type=int)
        accept_animal_with_chronic_illness = data.get("nChronicIllness", type=int)
        tutor_owns_animals = data.get("nHaveAnimals", type=int)
        tutor_has_time_availability = data.get("nTimeAvailability", type=int)

        # Filter user preferences
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
        qtde_animals = len(animals_list)
        return render_template("list_animal.html", animals_list=animals_list,
                               status_list=status_list, qtde_animals=qtde_animals)
    except Exception as e:
        message_error = "Erro ao listar os animais!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return redirect(url_for("animal.animals_list"))


@bp.route("/detail", methods=["GET", "POST"])
@login_required
def animal_detail():
    try:
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
    except Exception as e:
        message_error = "Erro ao adotar o animal!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return redirect(url_for("animal.animals_list"))


@bp.route("/adopt", methods=["POST"])
@login_required
def adopt_animal():
    try:
        if not current_user.is_adopter():
            flash("Somente usuários adotantes podem adotar animais!", "warning")
            return redirect(url_for("animal.animal_detail"))

        animal_id = int(session['animal_id'])

        user_filter = session.get("user_preferences_filter")
        animal = animal_service.get_animal_by_id(animal_id)

        # Check animal status
        if animal.status.value != "Disponivel":
            message = f"O animal não está disponível para adoção ou já foi adotado por outra pessoa!"
            flash(message, "warning")
            return render_template("detail_animal.html", animal=animal)

        # Check compatibility between animal and owner
        user_animals_list = user_service.get_animals_by_user(current_user.id)
        tutor_owns_animals = user_filter.get("tutor_owns_animals")
        if not animal.animal_adapt and (user_animals_list or tutor_owns_animals):
            message = f"Infelizmente {animal.name} não se adapta com animais, e você já possui animais!"
            flash(message, "warning")
            return render_template("detail_animal.html", animal=animal)

        # Check owner time availability
        tutor_has_time_availability = user_filter.get("tutor_time_availability")
        if not tutor_has_time_availability and animal.continuous_treatments:
            message = f"Esse animal exige cuidados constantes e você não possui tempo livre!"
            flash(message, "warning")
            return render_template("detail_animal.html", animal=animal)

        user_service.adopt_animal(current_user, animal)

        flash(f"Parabéns! Você adotou o {animal.name}!", "success")
        return redirect(url_for("animal.animal_detail"))
    except Exception as e:
        message_error = "Erro ao adotar o animal!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return redirect(url_for("animal.animal_detail"))

@bp.route("/report", methods=["GET"])
@login_required
def user_animal_report():
    try:
        animals_list = user_service.get_animals_by_user(current_user.id)

        qtde_animals = len(animals_list)
        session.page_title = "Meus animais"

        return render_template("user_animals_list.html", **locals())
    except Exception as e:
        message_error = "Erro ao consultar os animais do adotante!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return redirect(url_for("animal.animals_list"))
