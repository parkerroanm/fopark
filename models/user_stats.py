from db import db


class User_StatsModel(db.Model):
	__tablename__ = 'User_Stats'

	id = db.Column(db.Integer,primary_key=True)
	user_id = db.Column(db.Integer)
	rt_time = db.Column(db.Integer)
	ct_time = db.Column(db.Integer)
	request_sum = db.Column(db.Integer)
	pic_sum = db.Column(db.Integer)
	

	def __init__(self,user_id,rt_time,ct_time,request_sum,pic_sum):
		self.user_id = user_id
		self.rt_time = rt_time
		self.ct_time = ct_time
		self.request_sum = request_sum
		self.pic_sum = pic_sum

	def json(self):
		return {'user_id': self.user_id,'rt_time':self.rt_time,'ct_time':self.ct_time,'request_sum':self.request_sum,'pic_sum':self.pic_sum}

	@classmethod
	def find_by_user_id(cls,user_id):
		return cls.query.filter_by(user_id=user_id).first() #SELECT * FROM items WHERE name=name LIMIT 1

	def update_request_sum(self,user_id,request_sum):
		pass

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
	