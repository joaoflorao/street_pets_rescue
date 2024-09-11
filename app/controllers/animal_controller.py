from flask import Blueprint, request, render_template, flash, redirect, url_for
from app import animal_service

bp = Blueprint("animal", __name__)


@bp.route("/register", methods=["GET", "POST"])
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
