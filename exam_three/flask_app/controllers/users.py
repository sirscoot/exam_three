from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
	return redirect("/login")


@app.route("/login")
def login():
	return render_template("login.html")


@app.route("/login_handler", methods=["POST"])
def login_handler():
	data = {
		"email": request.form['email']
	}

	user = User.get_by_email(data)

	if not user:
		flash("Invalid email/password", "login")
		return redirect("/")
	if not bcrypt.check_password_hash(user.password, request.form['password']):
		flash("Invalid password", "login")
		return redirect("/")
	session['user_id'] = user.id
	return redirect("/dashboard")



@app.route("/register", methods=["POST"])
def register_handler():
	if not User.validator(request.form):
		return redirect("/")

	new_user = {
		"first_name": request.form['first_name'],
		"last_name": request.form['last_name'],
		"email": request.form['email'],
		"password": bcrypt.generate_password_hash(request.form['password'])
	}

	id = User.save(new_user)
	session['user_id'] = id
	return redirect("/dashboard")


@app.route("/logout")
def logout():
	session.clear()
	return redirect("/login")