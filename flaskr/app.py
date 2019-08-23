from flask import Flask, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, Google
# from authlib.jose import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import os
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# print(os.getenv('GOOGLE_CLIENT_ID'),os.getenv('GOOGLE_CLIENT_SECRET'))
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

oauth = OAuth(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, nullable=False)
    is_driver = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer, default=1)
    phone_number = db.Column(db.Integer)
    address_id = db.Column(db.String)
    address_show_txt = db.Column(db.String)


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


def handle_authorize(remote, token, user_info):
    email = user_info.email
    name = user_info.name
    # print(email, name)

    # add to db
    u = User(name=user_info.name, email=user_info.email)
    db.session.add(u)
    db.session.commit()

    # generating jwt
    # header = {'alg': 'RS256'}
    # iss = user_info['iss']
    # aud = user_info['aud']
    # sub = user_info['sub']
    # iat = user_info['iat']
    # exp = user_info['exp']
    # payload = {'iss': iss, 'sub': sub, 'aud': aud, 'iat': iat, 'exp': exp}
    # key = os.getenv('SECRET_KEY')
    # s = jwt.encode(header, payload, key)
    # jt = token['id_token']
    # print(jt)
    access_token = create_access_token(email)

    return jsonify(access_token)


google_bp = create_flask_blueprint(Google, oauth, handle_authorize)
app.register_blueprint(google_bp, url_prefix='/google')
