from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/full_stack_vrp"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Rider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(59))




if os.getenv("FLASK_ENV") == "development":
    @app.route('/')
    def index():
        return send_from_directory("static", "index.html")


    @app.route('/js/<file>')
    def js(file):
        return send_from_directory("static/js/", file)


    @app.route('/css/<file>')
    def css(file):
        return send_from_directory("static/css/", file)


    @app.route('/img/<file>')
    def img(file):
        return send_from_directory("static/img/", file)
