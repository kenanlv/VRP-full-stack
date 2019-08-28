import flask
from flask import Flask, send_from_directory, jsonify, render_template
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
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    is_driver = db.Column(db.Boolean, default=False)
    will_present = db.Column(db.Boolean, default=False)
    capacity = db.Column(db.Integer, default=1)
    phone_number = db.Column(db.String, default="N/A")
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


@app.route('/api/info', methods=['GET', 'POST'])
@jwt_required
def get_update_user_info():
    # global flg
    if flask.request.method == 'GET':
        current_user_email = get_jwt_identity()
        print('GET')
        print(current_user_email)
        user_get = User.query.filter_by(email=current_user_email).first()
        if user_get is not None:
            return row2dict(user_get)
        else:
            return {'email': current_user_email}
    else:
        print("POST")
        print(flask.request.is_json)
        print(flask.request.get_json())
        jason = flask.request.get_json()
        flg = False
        find_user = User.query.filter_by(email=jason['email']).first()
        print(find_user)
        if not find_user:
            flg = True
            find_user = User()
        find_user.name = jason['name']
        find_user.email = jason['email']
        find_user.is_driver = jason['is_driver'] == 'True'
        find_user.capacity = int(jason['capacity']) if jason['is_driver'] == 'True' else 1
        find_user.will_present = jason['will_present'] == 'True'
        # find_user.phone_number = int(jason['phone_number']) if jason['phone_number'] != 'None' and jason['phone_number'][0] != '0' else "hello"
        find_user.phone_number = jason['phone_number']
        find_user.address_id = jason['address_id']
        find_user.address_show_txt = jason['address_show_txt']
        if flg:
            db.session.add(find_user)
        db.session.commit()
        return 'OK'
    # arr = {}
    # all_users = User.query.all()
    # print(user_get.all())
    # i = 0
    # for user in all_users:
    #     # dict[ret.id] = vars(ret)
    #     arr[i] = row2dict(user)
    #     # print(arr[i])
    #     i += 1
    # return arr


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    # for column in row.all():
    #     print(column)
    #     # d[column] = str(getattr(row, column))

    return d


def handle_authorize(remote, token, user_info):
    email = user_info.email
    u_name = user_info.name
    print(email, u_name)

    # add to db
    u = User(name=user_info.name, email=user_info.email, will_present=True)

    exists = db.session.query(User.id).filter_by(name=u_name).scalar()
    # print(exists)

    # exists is not None
    if not exists:
        db.session.add(u)
        db.session.commit()
    else:
        x = db.session.query(User).get(exists)
        x.will_present = True
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

    access_token = create_access_token(email, expires_delta=False)  # change expires_delta back for expiration of token

    return render_template('jwt_redirect.html', jwt=str(access_token))


google_bp = create_flask_blueprint(Google, oauth, handle_authorize)
app.register_blueprint(google_bp, url_prefix='/google')
