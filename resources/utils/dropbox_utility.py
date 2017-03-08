#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dropbox
import cv2
import os
import time
import tempfile
from types import *
import numpy as np
from datetime import datetime, timedelta
from multiprocessing import Process
from threading import Thread

class TransferData:
	def __init__(self, access_token):
		self.access_token = access_token
		self.old_frame = None
		self.dbx = dropbox.Dropbox(self.access_token)
		self.prev_times = {}
		self.mod_times = {}
		self.image_output = {}
		self.data_output = {}


	def frozen_frame(self,frame):
		flag = False
		if self.old_frame is not None:
			dif_frame = cv2.absdiff(frame,self.old_frame)
			diff_sum = dif_frame.sum()
			if diff_sum == 0:
				flag = True
		self.old_frame = frame
		return flag
        
	def img_upload(self, file_from, file_to,image_str):
		"""upload a file to Dropbox using API v2"""
		overwrite = dropbox.files.WriteMode('overwrite',None)
		dbx = dropbox.Dropbox(self.access_token) 
		try: 
			if (type(file_from) == str):
				with open(file_from, 'rb') as f:
					dbx.files_upload(f,(file_to+image_str),mode = overwrite)
			else:
				jpg_string = cv2.imencode('.jpg',file_from)[1].tostring()
				dbx.files_upload(jpg_string,(file_to+image_str),mode = overwrite)
				#jpg.close()
				del dbx
				print "Image Uploaded"
		except Exception, err:
				print err
				del dbx

	def text_upload(self,text_from,file_to,file_name,path_flag = False):
		overwrite = dropbox.files.WriteMode('overwrite',None)
		dbx = dropbox.Dropbox(self.access_token)	
		try:
			if path_flag: 
				with open(text_from+file_name,'rb') as f: 
					dbx.files_upload(f,(file_to+file_name),mode = overwrite)
			else:
				text = text_from.encode(encoding='UTF-8',errors='strict')
				dbx.files_upload(text,(file_to+file_name),mode = overwrite)
				del dbx
				print "Text Uploaded"
		except Exception, err:
				print err
				del dbx

	def list_files(self,path):
		dbx = dropbox.Dropbox(self.access_token)
		output = []
		try:
			files_list = dbx.files_list_folder(path).entries
			for files in files_list:
				output.append(str(files.name))	
		except:
			print "Could Not List Files: Check Connection, Path, and Access Token"
			output = None
		return output

	def file_exists(self,path):
		output = None
		try:
			self.dbx.files_get_metadata(path)
			output =  True
		except:
			output =  False
			print "File Does Not Exist or Bad Connection"
		return output

	def delete_file(self,path):
		dbx = dropbox.Dropbox(self.access_token)	
		try: 
			response = dbx.files_delete(path)
			return response
			del dbx
		except Exception, err: 
			print err
			del dbx

	def batch_delete(self,filename_list,directory = None):
		dbx = dropbox.Dropbox(self.access_token)
		try: 
			if directory == None: 
				response = dbx.files_delete_batch(filename_list)
				return response
				del dbx
			else:
				path_list = []
				for name in filename_list:
					full_path = directory + name
					path_list.append(full_path)
				response = dbx.files_delete_batch(path_list)
				return response
				del dbx
		except Exception, err: 
			print "ERROR: {}".format(err)
			del dbx


	def download_file(self,path):
		dbx = dropbox.Dropbox(self.access_token)
		try: 
			md, res = dbx.files_download(path)
		except dropbox.exceptions.HttpError as err:
			print err
			return None

		data = res.content

		if ".jpg" in path or ".png" in path:
			data = np.fromstring(data,np.uint8)
			data = cv2.imdecode(data,1)
		return data

	def server_modified(self,path):
		#return number of seconds since UTC_DATETIME
		utc_datetime = datetime(1970,1,1)
		dbx = dropbox.Dropbox(self.access_token)
		try: 
			time = dbx.files_get_metadata(path).server_modified
		except dropbox.exceptions.HttpError as err:
			print err
			return None

		return (time-utc_datetime).total_seconds()

	def local_modified(self,local_path,folder_path = False):
		if (folder_path == False):
			time = os.listdir(local_path)
			return time
		else: 
			file_list = os.listdir(local_path)
			for items in file_list: 
				prev_times[items] = os.path.getmtime(local_path+items)
			return file_list

	def config_uploader(self,clientName,lotName):
		local_path = "Configuration_Files/"
		upload_path = "/fopark/Remote_Monitoring/{0}/{1}/Config_Files/".format(clientName,lotName)
		file_list = os.listdir(local_path)
		
		print file_list
		try:
			for file_name in file_list: 
				if ".txt" in file_name:
					self.text_upload(local_path,upload_path,file_name,path_flag = True)
					print "File: {0} uploaded!".format(file_name)

			server_list = self.list_files(upload_path)
			for items in server_list: 
				if ".txt" in items: 
					self.prev_times[items] = self.server_modified(upload_path+items)
		except: 
			print "Could Not UPLOAD Config Files"
	
	def data_writer(self,data,local_path,file_name):
		if not (os.path.exists(local_path)):
			os.makedirs(local_path)
		with open(local_path+file_name,'w') as f:
			f.write(data)

	def config_downloader(self,clientName,lotName):
		local_path = "Configuration_Files/"
		download_path = "/fopark/Remote_Monitoring/{0}/{1}/Config_Files/".format(clientName,lotName)

		file_list = self.list_files(download_path)
		try: 
			for items in file_list: 
				data = self.download_file(download_path+items)
				self.data_write(data,local_path,items)
		except:
			print "Could Not DOWNLOAD Config Files"

	def config_monitor(self,clientName,lotName):
		local_path = "Configuration_Files/"
		folder_path = "/fopark/Remote_Monitoring/{0}/{1}/Config_Files/".format(clientName,lotName)
		file_list = self.list_files(folder_path)
		local_file_list = self.local_modified(local_path,folder_path = True)
		reboot_flag = False

		try: 
			for items in file_list:
				if ".txt" in items:
					self.mod_times[items] = self.server_modified(folder_path+items)

					if (self.mod_times.get(items) > self.prev_times.get(items)) or (self.prev_times.get(items) == None):
						data = self.download_file(folder_path+items)
						self.data_writer(data,local_path,items)
						print "updating..."

					self.prev_times[items] = self.mod_times.get(items)
		except:
			print "Error in config_monitor: dropbox_utility"

	def comp_hist_uploader(self,clientName,lotName,unitName = None):
		local_path = "Configuration_Files/Comp_Hist/"
		upload_path = "/fopark/Remote_Monitoring/{0}/{1}/Config_Files/".format(clientName,lotName)
		file_list = os.listdir(local_path)
		print file_list
		try:
			for file_name in file_list: 
				if ".txt" in file_name:
					self.text_upload(local_path,upload_path,file_name,path_flag = True)
					print "File: {0} uploaded!".format(file_name)

			server_list = self.list_files(upload_path)
			for items in server_list: 
				if ".txt" in items: 
					self.prev_times[items] = self.server_modified(upload_path+items)
		except: 
			print "Could Not UPLOAD Config Files"

	def remote_image_monitor(self,folder_path,file_list):
		try: 
			for items in file_list:
				if ".jpg" in items:
					self.mod_times[items] = self.server_modified(folder_path+items)

					if (self.mod_times.get(items) != self.prev_times.get(items)) or (self.prev_times.get(items) == None):
						print("UPDATING.......{0}".format(items))
						self.image_output[items] = self.download_file(folder_path+items)
					self.prev_times[items] = self.mod_times.get(items)
		except: 
			print "remote_image_monitor: ERROR NOTHING RETURNED"
			return None
		return  self.image_output

	def remote_data_monitor(self,folder_path,file_list):
		try: 
			for items in file_list:
				if (".txt" in items) and ("Camera" in items):
					self.mod_times[items] = self.server_modified(folder_path+items)

					if (self.mod_times.get(items) != self.prev_times.get(items)) or (self.prev_times.get(items) == None):
						print("UPDATING.......{0}".format(items))
						self.data_output[items] = self.download_file(folder_path+items)
					self.prev_times[items] = self.mod_times.get(items)
		except: 
			print "remote_data_monitor: ERROR NOTHING RETURNED"
			return None
		return  self.data_output

	def time_average(self,Iters=10,):
		access_token = 'W5e_ns90DGkAAAAAAAANyXLi2fQzu9HW2RigHhQe-MzIla2co40WVVDSsFWbPZLG'

		frame = cv2.imread('image5.jpg')
		image_str = 'dropbox.jpg'
		file_to = '/fopark/Status_Photos/Deck_Test/'  # The full path to upload the file to, including the file name

		# API v2
		array = []
		for i in xrange(Iters):
			t0 = time.time()
			self.upload_file(frame, file_to,image_str)
			t1 = time.time()
			tsum = t1-t0
			array.append(tsum)
			time.sleep(1)
	
		b = sum(array)
		avg = b/(len(array))

		print ("Time Average: {0}".format(avg))


class Dropbox_Upload(Thread):
	def __init__(self,access_token, file_from, file_to,file_name,type_flag = 'IMAGE',image_type = '.png',path_flag = False):
		#parent class
		#Process.__init__(self)
		Thread.__init__(self)

		self.access_token = access_token
		self.file_from = file_from
		self.file_to = file_to
		self.file_name = file_name
		self.type_flag = type_flag
		self.path_flag = path_flag
		self.image_type = image_type

		
	def img_upload(self, file_from, file_to,image_str):
		"""upload a file to Dropbox using API v2"""
		overwrite = dropbox.files.WriteMode('overwrite',None)
		dbx = dropbox.Dropbox(self.access_token) 
		try: 
			if (type(file_from) == str):
				with open(file_from, 'rb') as f:
					dbx.files_upload(f,(file_to+image_str),mode = overwrite)
			else:
				jpg_string = cv2.imencode(self.image_type,file_from)[1].tostring()
				dbx.files_upload(jpg_string,(file_to+image_str),mode = overwrite)
				#jpg.close()
				del dbx
				print "Image Uploaded"
		except Exception, err:
				print err
				del dbx

	def text_upload(self,text_from,file_to,file_name,path_flag = False):
		overwrite = dropbox.files.WriteMode('overwrite',None)
		dbx = dropbox.Dropbox(self.access_token)	
		try:
			if path_flag: 
				with open(text_from+file_name,'rb') as f: 
					dbx.files_upload(f,(file_to+file_name),mode = overwrite)
			else:
				text = text_from.encode(encoding='UTF-8',errors='strict')
				dbx.files_upload(text,(file_to+file_name),mode = overwrite)
				del dbx
				print "Text Uploaded"
		except Exception, err:
				print err
				del dbx

	def run(self):
		if self.type_flag == 'IMAGE':
			self.img_upload(self.file_from,self.file_to,self.file_name)
		elif self.type_flag == 'TEXT':
			self.text_upload(self.file_from,self.file_to,self.file_name,self.path_flag)


class Dropbox_Img_Download(Process):
	def __init__(self,path,name,access_token,pipe_send):
		Process.__init__(self)
		self.access_token = access_token
		self.path = path
		self.name = name
		self.data = None
		self.dbx = dropbox.Dropbox(self.access_token)
		self.time_mod = None
		self.success = True
		self.pipe_send = pipe_send

	def download_file(self,path):
		try: 
			md, res = self.dbx.files_download(path)
			self.success = True
		except dropbox.exceptions.HttpError as err:
			print err
			self.success = False
			return None


		data = res.content

		if ".jpg" in path or ".png" in path:
			data = np.fromstring(data,np.uint8)
			data = cv2.imdecode(data,1)
		return data

	def delete_file(self,path):
		utc_datetime = datetime(1970,1,1)
		try: 
			response = self.dbx.files_delete(path)
			time = response.server_modified
			self.success = True
			return (time-utc_datetime).total_seconds()
			
		except Exception, err: 
			self.success = False
			print err
			
	def run(self):
		self.data = self.download_file(self.path+self.name)
		if self.success:
			self.time_mod = self.delete_file(self.path+self.name)
		result = [self.name,self.data,self.time_mod,self.success]
		self.pipe_send.send(result)

	'''def join(self):
		Process.join(self)
		
		#return self.name, self.data, self.time_mod, self.success'''
