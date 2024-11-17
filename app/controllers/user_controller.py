from flask import Blueprint, request, render_template, flash, session, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from app import user_service
from app import app

bp = Blueprint("user", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "GET":
            return render_template("login.html")

        data = request.form
        email = data.get("nEmail")
        password = data.get("nPassword")

        user = user_service.check_user_exists(email)
        if user and user.check_password(user.password, password):
            login_user(user)
            session['user_preferences_filter'] = {}
            return redirect(url_for("animal.animals_list"))

        flash("Usuário ou senha incorretos!", "danger")
        return render_template("login.html")
    except Exception as e:
        message_error = "Erro ao realizar o login!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@bp.route("/register", methods=["GET", "POST"])
def register():
    user_types_list = user_service.get_user_types_list()
    try:
        if request.method == "GET":
            return render_template("register_user.html", user_types_list=user_types_list)

        data = request.form
        name = data.get("nFullName")
        email = data.get("nEmail")
        password = data.get("nPassword")
        birth_date = data.get("nBirthDate")
        user_type = data.get("nUserType")

        user_exists = user_service.check_user_exists(email)
        if user_exists:
            flash("Email já cadastrado!", "warning")
            return redirect(url_for("user.login"))

        user_service.create_user(name, email, password, birth_date, user_type)

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("user.login"))
    except Exception as e:
        message_error = "Erro ao cadastrar o usuário!"
        app.logger.error("%s /error: %s", message_error, e)
        flash(message_error, "danger")
        return render_template("register_user.html", user_types_list=user_types_list)
