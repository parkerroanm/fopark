from keras.models import model_from_json
import numpy as np
import tensorflow as tf
from keras import backend as K

K.set_image_dim_ordering('th')

def model_loader(json_path,weights_path):
	# load json and create model
	json_file = open(json_path, 'r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)
	
	loaded_model.load_weights(weights_path)
	print("Loaded model from disk")

	# evaluate loaded model on test data
	loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	return loaded_model

def model_predictor(model,image,graph):
	with graph.as_default():
		result = model.predict_classes(image,verbose = 0)
		if result == 1: 
			return True
		return False
