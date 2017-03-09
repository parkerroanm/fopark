from flask_restful import Resource, reqparse
from models.PC import PCModel


class PC(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('client_id',
		type = str,
		required = True,
		help = 'Client Identifier'
		)
	parser.add_argument('lot_id',
		type=str,
		required = True,
		help = 'Lot Identifier'
		)
	parser.add_argument('unit_id',
		type=str,
		required = True,
		help = 'Unit Identifier'
		)
	parser.add_argument('serial_num',
		type = str,
		required = True,
		help = 'Time stamp of when modified'
		)

	
	def get(self,host_name):
		item = PCModel.find_by_host_name(host_name)
		if item: 
			return item.json()
		return {'message': 'Item not found'}, 404

	def post(self,host_name):
		data = PC.parser.parse_args()
		item = PCModel.find_by_host_name(host_name)

		if item:
			return {'message': 'A PC with name {} already exists'.format(host_name)}, 400

		store = PCModel(host_name,**data)

		try: 
			store.save_to_db()
		except: 
			return {'message': 'An error occured while creating the store.'}, 500

		return store.json(), 201
	
	def put(self,host_name):
		data = PC.parser.parse_args()
		item = PCModel.find_by_host_name(host_name)
		
		if item is None:
			item = PCModel(host_name,**data)
		else: 
			item.serial_num = data['serial_num']
		
		item.save_to_db()

		return item.json()
