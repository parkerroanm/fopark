from db import db


class StallModel(db.Model):
	__tablename__ = 'Stalls'

	id = db.Column(db.Integer,primary_key=True)
	lot_id = db.Column(db.String(80))
	stall_id = db.Column(db.Integer)
	cam_id = db.Column(db.String(80))
	status = db.Column(db.Integer)
	rt_time = db.Column(db.Integer) 
	

	def __init__(self,lot_id,stall_id,cam_id,status,rt_time):
		self.lot_id = lot_id
		self.stall_id = stall_id
		self.cam_id = cam_id
		self.status = status
		self.rt_time = rt_time

	def json(self):
		return {'lot_id': self.lot_id,'stall_id':self.stall_id,'cam_id':self.cam_id,'status':self.status,'rt_time':self.rt_time}

	@classmethod
	def find_by_stall_id(cls,lot_id,stall_id):
		return cls.query.filter_by(lot_id=lot_id,stall_id=stall_id).first() #SELECT * FROM items WHERE name=name LIMIT 1

	def update(self):
		pass

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	

