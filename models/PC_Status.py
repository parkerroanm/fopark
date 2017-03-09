from db import db


class PCStatModel(db.Model):
	__tablename__ = 'PC_Statuses'

	id = db.Column(db.Integer,primary_key=True)
	pc_id = db.Column(db.String,db.ForeignKey('PCs.host_name'))
	pc = db.relationship('PCModel')

	cpu_usg = db.Column(db.Float)
	cpu_sys = db.Column(db.Float)
	cpu_usr = db.Column(db.Float)
	ram_util = db.Column(db.Float)
	disk_util = db.Column(db.Float) 
	io_read = db.Column(db.Float)
	io_write = db.Column(db.Float)

	
	

	def __init__(self,pc_id,cpu_usg,cpu_sys,cpu_usr,ram_util,disk_util,io_read,io_write):
		self.pc_id = pc_id
		self.cpu_usg = cpu_usg
		self.cpu_sys = cpu_sys
		self.cpu_usr = cpu_usr
		self.ram_util = ram_util
		self.disk_util = disk_util
		self.io_read = io_read
		self.io_write = io_write


	def json(self):
		return {'PC_Name': self.pc_id,'cpu_usg':self.cpu_usg,'cpu_sys':self.cpu_sys,'cpu_usr':self.cpu_usr,'ram_util':self.ram_util,
			'disk_util':self.disk_util,'io_read':self.io_read,'io_write':self.io_write}

	@classmethod
	def find_by_pc_id(cls,pc_id):
		return cls.query.filter_by(pc_id=pc_id).first() #SELECT * FROM items WHERE name=name LIMIT 1

	def update(self):
		pass

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	
