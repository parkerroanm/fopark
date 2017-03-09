from flask_restful import Resource, reqparse
from models.PC_Status import PCStatModel


class PC_Status(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('cpu_usg',
		type = float,
		required = True,
		help = 'Total CPU Usage'
		)
	parser.add_argument('cpu_sys',
		type = float,
		required = True,
		help = 'Current System Usage'
		)
	parser.add_argument('cpu_usr',
		type = float,
		required = True,
		help = 'Current User Usage'
		)
	parser.add_argument('ram_util',
		type = float,
		required = True,
		help = 'Ram Memory Percentage'
		)
	parser.add_argument('disk_util',
		type = float,
		required = True,
		help = 'Memory Percentage'
		)
	parser.add_argument('io_read',
		type = float,
		required = True,
		help = 'Mbs Read'
		)
	parser.add_argument('io_write',
		type = float,
		required = True,
		help = 'Mbs Write'
		)
	
	def get(self,pc_id):
		item = PCStatModel.find_by_PC_id(PC_id)
		if item: 
			return item.json()
		return {'message': 'Item not found'}, 404

	def put(self,pc_id):
		data = PC_Status.parser.parse_args()
		item = PCStatModel.find_by_pc_id(pc_id)
		
		if item is None:
			item = PCStatModel(pc_id,**data)
		else: 
			item.cpu_usg = data['cpu_usg']
			item.cpu_sys = data['cpu_sys']
			item.cpu_usr = data['cpu_usr']
			item.ram_util = data['ram_util']
			item.disk_util = data['disk_util']
			item.io_read = data['io_read']
			item.io_write = data['io_write']




		item.save_to_db()

		return item.json()

