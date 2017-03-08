from flask_restful import Resource, reqparse
from models.stall import StallModel


class Stall(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('cam_id',
		type = str,
		required = True,
		help = 'Cam Identifier'
		)
	parser.add_argument('status',
		type=int,
		required = True,
		help = 'Stall Status'
		)
	parser.add_argument('rt_time',
		type = int,
		required = True,
		help = 'Time stamp of when modified'
		)
	
	def get(self,lot_id,stall_id):
		item = StallModel.find_by_stall_id(lot_id,stall_id)
		if item: 
			return item.json()
		return {'message': 'Item not found'}, 404

	def put(self,lot_id,stall_id):
		data = Stall.parser.parse_args()
		item = StallModel.find_by_stall_id(lot_id,stall_id)
		
		if item is None:
			item = StallModel(lot_id,stall_id,**data)
		else: 
			item.status = data['status']
		
		item.save_to_db()

		return item.json()
	
class Cam_Status(Resource):
	def get(self,lot_id,cam_id):
		return {'Cam_Status': [item.json() for item in StallModel.query.filter_by(lot_id=lot_id,cam_id=cam_id)]}

class Lot_Status(Resource):
	def get(self,lot_id):
		return {'Lot_Status': [item.json() for item in StallModel.query.filter_by(lot_id=lot_id)]}

