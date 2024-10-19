from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_required, current_user
from app import animal_history_service, animal_service

bp = Blueprint("animal_history", __name__)


@bp.route("/animal_history", methods=["GET", "POST"])
@login_required
def animal_history():
    data = request.form
    animal_id = data.get("nAnimalId")
    action_types_list = animal_history_service.get_event_types()

    animal = animal_service.get_animal_by_id(animal_id)
    animal_history = animal_history_service.get_animal_history(animal_id)

    return render_template("animal_history.html", **locals())


@bp.route("/register_event_history", methods=["GET", "POST"])
@login_required
def register_location():
    data = request.form
    action_types_list = animal_history_service.get_event_types()

    animal_id = data.get("nAnimalId")
    action_type = data.get("nActionType")
    description = data.get("nDescription")
    start_date = data.get("nStartDate")
    end_date = data.get("nEndDate")

    animal = animal_service.get_animal_by_id(animal_id)
    animal_history_service.add_animal_event_history(animal_id, action_type, description, start_date, end_date)
    animal_history = animal_history_service.get_animal_history(animal_id)

    return render_template("animal_history.html", **locals())
