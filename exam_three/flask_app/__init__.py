from flask import Flask

app = Flask(__name__)

app.secret_key = 'secret'


from flask_app.controllers import users, dashboard