from db import db


class PCModel(db.Model):
	__tablename__ = 'PCs'

	id = db.Column(db.Integer,primary_key=True)
	host_name = db.Column(db.String(80))
	client_id = db.Column(db.String(80))
	lot_id = db.Column(db.String(80))
	unit_id = db.Column(db.String(80))
	serial_num = db.Column(db.String(80))
	
	pcs = db.relationship('PCStatModel')
	
	def __init__(self,host_name,client_id,lot_id,unit_id,serial_num):
		self.host_name = host_name
		self.client_id = client_id
		self.lot_id = lot_id
		self.unit_id = unit_id
		self.serial_num = serial_num

	def json(self):
		return {'host_name': self.host_name,'client_id':self.client_id,'lot_id':self.lot_id,'unit_id':self.unit_id,'serial_num':self.serial_num}

	@classmethod
	def find_by_host_name(cls,host_name):
		return cls.query.filter_by(host_name=host_name).first() #SELECT * FROM items WHERE name=name LIMIT 1

	def update(self):
		pass

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	
