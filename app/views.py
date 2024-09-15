from app import app
from flask import Flask, render_template, url_for, request
from flask_login import login_required


@app.route("/")
@app.route("/login")
def login():
    return render_template("login.html")
