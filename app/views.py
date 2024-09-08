from app import app
from flask import Flask, render_template, url_for, request


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register_user.html")
