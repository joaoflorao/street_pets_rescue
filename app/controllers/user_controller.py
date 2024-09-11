from flask import Blueprint, request, render_template, flash, redirect, url_for
from app import user_service

bp = Blueprint("user", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    data = request.form
    email = data.get("nEmail")
    password = data.get("nPassword")

    user = user_service.check_user_exists(email)
    if user and user.check_password(user.password, password):
        flash("Usuário logado!", "success")

    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register_user.html")

    data = request.form
    name = data.get("nFullName")
    email = data.get("nEmail")
    password = data.get("nPassword")
    birth_date = data.get("nBirthDate")

    user_exists = user_service.check_user_exists(email)
    if user_exists:
        flash("Email já cadastrado!", "warning")
        return redirect(url_for("user.login"))

    user_service.create_user(name, email, password, birth_date)

    flash("Usuário cadastrado com sucesso!", "success")
    return redirect(url_for("user.login"))
