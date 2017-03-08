from flask import render_template
from flask_restful import Resource

class Home(Resource):
	def home(self):
		return render_template('index.html')