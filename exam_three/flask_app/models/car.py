from flask_app.config.connector import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models import user



class Car:
	DB = "car_sales"
	def __init__(self,data):
		self.id = data['id']
		self.make = data['make']
		self.model = data['model']
		self.year = data['year']
		self.description = data['description']
		self.price = data['price']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
		self.user_id = data['user_id']

		self.creator = None


	@classmethod
	def save(cls,data):
		query = "INSERT INTO cars (make,model,year,description,price,user_id) VALUES (%(make)s,%(model)s,%(year)s,%(description)s,%(price)s,%(user_id)s);"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def view(cls,data):
		query = "SELECT * FROM cars WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def delete(cls,data):
		query = "DELETE FROM cars WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def update(cls,data):
		query = "UPDATE cars SET make = %(make)s,model = %(model)s,year = %(year)s,description = %(description)s,price = %(price)s WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,data)
		return result


	@classmethod
	def get_by_id(cls,car_id):
		query = "SELECT * FROM cars WHERE id = %(id)s;"
		result = connectToMySQL(cls.DB).query_db(query,car_id)
		if result:
			car = cls(result[0])
			return car
		return False




	@classmethod
	def get_cars_with_sellers(cls):
		query = "SELECT * FROM cars LEFT JOIN users ON cars.user_id = users.id;"
		result = connectToMySQL(cls.DB).query_db(query)
		all_cars = []
		for row in result:
			one_car = cls(row)

			one_car_user_info = {
				"id": row['users.id'],
				"first_name": row['first_name'],
				"last_name": row['last_name'],
				"email": row['email'],
				"password": row['password'],
				"created_at": row['users.created_at'],
				"updated_at": row['users.updated_at']
			}

			seller = user.User(one_car_user_info)

			one_car.creator = seller

			all_cars.append(one_car)

		return all_cars