from db import db

class ImageModel(db.Model):
	__tablename__ = 'Image_Queue'

	id = db.Column(db.Integer,primary_key=True)
	binary = db.Column(db.LargeBinary(80))
	name = db.Column(db.Integer)
	time_stamp = db.Column(db.Integer) 
	

	def __init__(self,name,binary,time_stamp):
		self.name = name
		self.binary = binary
		self.time_stamp = time_stamp

	def json(self):
		return {'name': self.name,'binary':self.binary,'time_stamp':self.time_stamp}

	@classmethod
	def find_by_name(cls,name):
		return cls.query.filter_by(name=self.name).first() #SELECT * FROM items WHERE name=name LIMIT 1

	def update(self):
		pass

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

