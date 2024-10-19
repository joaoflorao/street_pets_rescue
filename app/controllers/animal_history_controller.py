from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_required, current_user
from app import animal_history_service, animal_service
from app.models.event_type import EventType

bp = Blueprint("animal_history", __name__)


@bp.route("/animal_history", methods=["GET", "POST"])
@login_required
def animal_history():
    data = request.form
    action_types_list = animal_history_service.get_event_types()
    status_list = animal_service.get_status_list()

    animal_id = data.get("nAnimalId", type=int)
    if request.method == "GET":
        animal = animal_service.get_animal_by_id(animal_id)
        animal_history = animal_history_service.get_animal_history(animal_id)
        return render_template("animal_history.html", **locals())

    animal = animal_service.get_animal_by_id(animal_id)
    animal_history = animal_history_service.get_animal_history(animal_id)

    return render_template("animal_history.html", **locals())


@bp.route("/register_event_history", methods=["GET", "POST"])
@login_required
def register_location():
    data = request.form
    action_types_list = animal_history_service.get_event_types()
    status_list = animal_service.get_status_list()

    animal_id = data.get("nAnimalId", type=int)
    if request.method == "GET":
        animal = animal_service.get_animal_by_id(animal_id)
        animal_history = animal_history_service.get_animal_history(animal_id)
        return render_template("animal_history.html", **locals())

    action_type = data.get("nActionType")
    description = data.get("nDescription")
    event_date = data.get("nEventDate")
    animal_new_status = data.get("nAnimalStatus")

    event_description = description
    animal = animal_service.get_animal_by_id(animal_id)
    if action_type == EventType.status.value:
        animal_service.update_animal_status(animal_id, animal_new_status)
        event_description = f"Animal {animal_new_status}. {description}"

    animal_history_service.add_animal_event_history(animal_id, action_type, event_description, event_date)
    animal_history = animal_history_service.get_animal_history(animal_id)

    return redirect(url_for('animal_history', animal_id=animal_id))
