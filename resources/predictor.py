from flask_restful import Resource, reqparse
from skimage import io
from skimage.transform import resize, rescale
from utils.image_utils import image_decoder, resize_image
from utils.model_utils import model_loader, model_predictor
import tensorflow as tf
import numpy as np
import os
import json
from keras import backend as K

K.set_image_dim_ordering('th')

class Car_Predictor(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('img_str',
		type=str,
		required = True,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('img_name',
		type=str,
		required = False,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('cam_id',
		type=str,
		required = False,
		help = "This field cannot be left blank!"
	)
	parser.add_argument('stall_id',
		type=str,
		required = False,
		help = "This field cannot be left blank!"
	)

	model = model_loader("./resources/CNNs/VG_car_model0.json","./resources/CNNs/VG_car_model0.h5")
	graph = tf.get_default_graph()
	def post(self):
		
		data = Car_Predictor.parser.parse_args()
		img_str = data.get('img_str')
		image = image_decoder(img_str)
		image = resize_image(image)

		response = model_predictor(Car_Predictor.model,image,Car_Predictor.graph)
		


		return json.dumps({"return": response})

