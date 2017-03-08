from flask_restful import Resource, reqparse
from models.user_stats import User_StatsModel


class User_Stats(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('rt_time',
		type = int,
		required = True,
		help = 'Average Response Time from DB to API'
		)
	parser.add_argument('ct_time',
		type=int,
		required = True,
		help = 'Average Response from Load to Submit'
		)
	parser.add_argument('request_sum',
		type= int, 
		required = True,
		help = 'Total Number of Requests Sent'
		)
	parser.add_argument('pic_sum',
		type= int, 
		required = True,
		help = 'Total Number of Photos Corrected'
		)

	def get(self,user_id):
		item = User_StatsModel.find_by_user_id(user_id)
		if item: 
			return item.json()
		return {'message': 'Item not found'}, 404

	def put(self,user_id):
		data = User_Stats.parser.parse_args()
		item = User_StatsModel.find_by_user_id(user_id)
		
		if item is None:
			item = User_StatsModel(user_id,**data)
		else: 
			item.rt_time = data['rt_time']
			item.ct_time = data['ct_time']
			item.request_sum = data['request_sum']
			item.pic_sum = data['pic_sum']
		
		item.save_to_db()

		return item.json()