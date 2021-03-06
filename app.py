import os
import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT
from db import db
from security import authenticate, identity as identity_function

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL", "sqlite:///data.db")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'janny'
api = Api(app) #adds resources easily

app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity_function)

app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800) #expire token 30 mins
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
 return jsonify({
 'access_token': access_token.decode('utf-8'),
 'user_id': identity.id
 })

# @jwt.error_handler
# def customized_error_handler(error):
#  return jsonify({
#  'message': error.description,
#  'code': error.status_code
#  }), error.status_code

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)