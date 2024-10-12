from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_required, current_user
from app import animal_location_service, animal_service

bp = Blueprint("animal_location_history", __name__)


@bp.route("/animal_history", methods=["GET", "POST"])
@login_required
def animal_history():
    data = request.form
    animal_id = data.get("nAnimalId")

    animal = animal_service.get_animal_by_id(animal_id)
    animal_location_history = animal_location_service.get_location_history(animal_id)

    return render_template("animal_history.html", **locals())


@bp.route("/register_location", methods=["GET", "POST"])
@login_required
def register_location():
    data = request.form

    animal_id = data.get("nAnimalId")
    location = data.get("nLocation")
    start_date = data.get("nStartDate")
    end_date = data.get("nEndDate")

    animal = animal_service.get_animal_by_id(animal_id)
    animal_location_service.add_animal_location(animal_id, location, start_date, end_date)
    animal_location_history = animal_location_service.get_location_history(animal_id)

    return render_template("animal_history.html", **locals())
