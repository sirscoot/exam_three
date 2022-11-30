from flask import Flask, render_template, session, redirect, request, flash
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.car import Car



@app.route("/dashboard")
def dashboard():
	if 'user_id' not in session:
		flash("You must be logged in to view this page", "login")
		return redirect("/login")

	data = {
		"id": session['user_id']
	}

	current_user = User.get_one(data)
	cars_for_sale = Car.get_cars_with_sellers()
	return render_template("dashboard.html",cars=cars_for_sale, current_user=current_user)



@app.route("/new_car")
def new():
	if 'user_id' not in session:
		flash("You must be logged in to view this page", "login")
		return redirect("/login")
	return render_template("new.html")


@app.route("/save", methods=['POST'])
def save():
	if 'user_id' not in session:
		flash("You must be logged in to view this page", "login")
		return redirect("/login")

	data = {
		"price": request.form['price'],
		"model": request.form['model'],
		"make": request.form['make'],
		"year": request.form['year'],
		"description": request.form['description'],
		"user_id": request.form['user_id']
	}
	

	if len(data['model']) < 1 or len(data['make']) < 1 or len(data['description']) < 1:
		flash("All fields must be filled in", "add")
		return redirect("/new_car")
	if len(data['year']) < 1:
		flash("Year must be larger than 0", "add")
		return redirect("/new_car")
	if len(data['price']) < 1:
		flash("Price cannot be 0", "add")
		return redirect("/new_car")

	Car.save(data)
	return redirect("/dashboard")

@app.route("/edit/<int:car_id>")
def edit_car(car_id):
	data = {
		"id": car_id
	}
	edit_car = Car.get_by_id(data)
	return render_template("edit.html", car=edit_car)


@app.route("/update/<int:car_id>", methods=['POST'])
def update(car_id):
	data = {
		"id": car_id,
		"price": request.form['price'],
		"model": request.form['model'],
		"make": request.form['make'],
		"year": request.form['year'],
		"description": request.form['description'],
		"user_id": session['user_id']
	}

	
	if len(data['model']) < 1 or len(data['make']) < 1 or len(data['description']) < 1:
		flash("All fields must be filled in", "edit")
		return redirect(f"/edit/{car_id}")
	if len(data['year']) < 1:
		flash("Year must be larger than 0", "edit")
		return redirect(f"/edit/{car_id}")
	if len(data['price']) < 1:
		flash("Price cannot be 0", "edit")
		return redirect(f"/edit/{car_id}")


	Car.update(data)
	return redirect("/dashboard")


@app.route("/show/<int:car_id>")
def show_car(car_id):
	data = {
		"id": car_id
	}
	cars = Car.get_by_id(data)

	return render_template("show.html", cars=cars)




@app.route("/delete/<int:car_id>")
def delete_car(car_id):
	if "user_id" not in session:
		flash("you must be logged in to view this page", "login")
		return redirect("/login")
	data = {
		"id": car_id
	}

	Car.delete(data)
	return redirect("/dashboard")