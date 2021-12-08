# coding=utf8

import random
import string
import time
import json

from eth_account.messages import defunct_hash_message
from flask import render_template, request, Flask, abort, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, set_access_cookies
from flask_sqlalchemy import SQLAlchemy
from web3.auto import w3

from ethhelper import multi_send, get_receipt, gstAddress

app = Flask(__name__, static_url_path='/static')
app.jinja_env.add_extension('jinja2.ext.do')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = ''.join(random.choice(string.ascii_lowercase) for i in range(22))
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
# app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
jwt = JWTManager(app)


@app.before_first_request
def setup():
    try:
        db.create_all()
    except:
        print("[+] users db already exists")


def generate_nonce(self, length=8):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


class User(db.Model):
    public_address = db.Column(db.String(80), primary_key=True, nullable=False, unique=True)
    nonce = db.Column(db.Integer(), nullable=False, default=generate_nonce, )


@app.route('/')
def landing():
    return render_template("index.html")


@app.route('/receipt', methods=['POST'])
@jwt_required()
def receipt():
    receipt_hash = request.json[0]
    print(receipt_hash)
    receipt_logs = get_receipt(receipt_hash, "")
    print(receipt_logs)
    return json.dumps([dict(x.args) for x in receipt_logs if x.event == "Sent" and x.address == gstAddress])


@app.route('/multi_send')
@jwt_required()
def secret():
    current_user = get_jwt_identity()
    val = multi_send([
        "0x28cde2620eCaD7AB9Fb4BD0C362C02FF4b1D12D3", 
        "0x4b44af050203Ee6539cb4b92F88E5852ad53741B"
    ], [
        1000000000000000,
        1000000000000000
    ], 2000000000000000, current_user)
    print(val["data"])
    return json.dumps(val)


@app.route('/login', methods=['POST'])
def login():
    public_address = request.json[0]
    signature = request.json[1]
    domain = "192.168.122.1"
    rightnow = int(time.time())
    sortanow = rightnow - rightnow % 600
    original_message = 'Signing in to {} at {}'.format(domain, sortanow)
    message_hash = defunct_hash_message(text=original_message)
    signer = w3.eth.account.recoverHash(message_hash, signature=signature)
    if signer == public_address:
        print("[+] this is fine " + str(signer))
        # account.nonce = account.generate_nonce()
        # db.session.commit()
    else:
        abort(401, 'could not authenticate signature')
    access_token = create_access_token(identity=public_address)

    resp = jsonify({'login': True, "access_token": access_token})
    set_access_cookies(resp, access_token)
    return resp, 200
