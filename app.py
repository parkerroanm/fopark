import os

from flask import Flask, render_template, url_for
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate,identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store,StoreList
from resources.home import Home
from resources.stall import Stall, Cam_Status, Lot_Status
from resources.user_stats import User_Stats
from resources.predictor import Car_Predictor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'
api = Api(app)

#Uncommit below if you are running locally
@app.before_first_request
def create_tables(): 
	db.create_all()

jwt = JWT(app,authenticate, identity) #/auth

'''@app.route('/')
def home(): 
	return render_template('index.html')'''
api.add_resource(Car_Predictor,'/predictor')
api.add_resource(Stall,'/stall/<string:lot_id>/<int:stall_id>')
api.add_resource(Lot_Status,'/lot/<string:lot_id>')
api.add_resource(Cam_Status,'/cam/<string:lot_id>/<string:cam_id>')
api.add_resource(User_Stats,'/user_stats/<string:user_id>')


if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug = True)