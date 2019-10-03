import flask
from flask import Flask, render_template
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint, Google
import time
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

import requests
from models import User
from database import db_session
from json import loads
import re

import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql:postgres:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
START_TIME = os.getenv("SOLVER_START_TIME")

oauth = OAuth(app)
jwt = JWTManager(app)


@app.route('/api/info', methods=['GET', 'POST'])
@jwt_required
def get_update_user_info():
    if flask.request.method == 'GET':
        current_user_email = get_jwt_identity()
        user_get = db_session.query(User).filter_by(email=current_user_email).first()
        if user_get is not None:
            return row2dict(user_get)
        else:
            return {'email': current_user_email}
    else:
        json = flask.request.get_json()
        t = time.asctime().split(' ')
        if (t[0] == 'Sat' and int(t[3][0:2]) > START_TIME) or t[0] == 'Sun':
            return "Sorry, you could not sign up for the riding system after Saturday noon.", 400
        find_user = db_session.query(User).filter_by(email=json['email']).first()
        find_user.name = json['name']
        find_user.is_driver = json['is_driver'] == 'True'
        find_user.capacity = int(json['capacity']) if json['is_driver'] == 'True' else 1
        find_user.will_present = json['will_present'] == 'True'
        find_user.phone_number = json['phone_number']
        find_user.address_id = json['address_id']
        find_user.address_show_txt = json['address_show_txt']
        user = validate_user(find_user)
        if user:
            db_session.commit()
            return 'OK'
        else:
            return 'Invalid parameter', 400


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def api_builder(id):
    return f"https://maps.googleapis.com/maps/api/place/details/json?" \
           f"place_id={id}&" \
           f"key={os.getenv('API_KEY_DIS')}&" \
           f"fields=place_id"


def validate_user(user: User):
    if len(user.name.strip()) == 0:
        return False
    if not re.match('^\d{10}$', user.phone_number):
        return False
    if not 0 < user.capacity < 6:
        return False
    if len(user.address_show_txt.strip()) == 0:
        return False
    response = requests.get(api_builder(user.address_id)).json()
    if response['status'] == 'OK':
        user.address_id = response['result']['place_id']
        return user
    else:
        return False


def handle_authorize(remote, token, user_info):
    email = user_info.email
    u_name = user_info.name
    print(email, u_name)

    # add to db
    u = User(name=user_info.name, email=user_info.email, will_present=False)

    exists = db_session.query(User.id).filter_by(name=u_name).scalar()

    # exists is not None
    if not exists:
        db_session.add(u)
        db_session.commit()
    else:
        x = db_session.query(User).get(exists)
        x.will_present = True
        db_session.commit()

    # generating jwt
    access_token = create_access_token(email, expires_delta=False)
    return render_template('jwt_redirect.html', jwt=str(access_token))


google_bp = create_flask_blueprint(Google, oauth, handle_authorize)
app.register_blueprint(google_bp, url_prefix='/google')
