from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app import animal_service, user_service

bp = Blueprint("animal", __name__)


@bp.route("/register", methods=["GET", "POST"])
@login_required
def register():
    status_list = animal_service.get_status_list()
    if request.method == "GET":
        return render_template("register_animal.html", status_list=status_list)

    data = request.form
    animal_name = data.get("nAnimalName")
    animal_type = data.get("nAnimalType")
    characteristics = data.get("nCharacteristics")
    health_needs = data.get("nHealthNeeds")
    continuous_treatments = data.get("nContinuousTreatments")
    special_needs = data.get("nSpecialNeeds")
    animal_status = data.get("nAnimalStatus")
    rescue_date = data.get("nRescueDate")

    animal_service.register_animal(
        animal_name, animal_type, characteristics, health_needs,
        continuous_treatments, special_needs, animal_status, rescue_date,
    )

    flash("Animal cadastrado com sucesso!", "success")
    return render_template("register_animal.html", status_list=status_list)


@bp.route("/list", methods=["GET", "POST"])
@login_required
def animals_list():
    if request.method == "GET":
        animals_list = animal_service.get_animals_list("available")
        return render_template("list_animal.html", animals_list=animals_list)

    data = request.form

    animal_specie = data.get('nSpecie')
    animal_size = data.get('nSize')
    animal_sex = data.get('nSex')
    animal_continuous_treatment = data.get('nTreatment')
    animal_chronic_illness = data.get('nChronicIllness')
    tutor_already_has_animals = data.get('nHaveAnimals')
    tutor_has_time_availability = data.get('nTimeAvailability')

    animals_list = animal_service.get_animals_list("available")
    return render_template("list_animal.html", animals_list=animals_list)


@bp.route("/detail/<int:animal_id>", methods=["GET"])
@login_required
def animal_detail(animal_id):
    animal_info = animal_service.get_animal_by_id(animal_id)
    if not animal_info:
        flash("Animal não encontrado", "warning")
        return redirect(url_for("animal.animals_list"))

    return render_template("detail_animal.html", animal=animal_info)


@bp.route("/adopt", methods=["POST"])
@login_required
def adopt_animal():
    data = request.form
    animal_id = data.get("nAnimalId")

    animal = animal_service.get_animal_by_id(animal_id)
    if animal.status.value != "Disponivel":
        flash("O animal não está disponível para adoção!", "warning")
        return render_template("detail_animal.html", animal=animal)

    new_animal_status = "Adotado"
    animal = animal_service.update_animal_status(animal_id, new_animal_status)
    user_service.adopt_animal(current_user, animal)

    flash(f"Parabéns! Você adotou o {animal.name}!", "success")
    return render_template("detail_animal.html", animal=animal)
