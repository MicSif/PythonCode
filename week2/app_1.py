#!/usr/bin/env python3
from flask import Flask,render_template,abort
import os,json,os.path
app=Flask(__name__)
@app.route('/')
def index():
	path_file='/home/shiyanlou/files/'
	file_list=os.listdir(path_file)
	json_name=[]
	for each_file in file_list:
		if each_file.split('.')[1]=='json':
			with open(path_file+each_file) as json_file:
				json_data=json.load(json_file)
				json_name.append(json_data.get('title'))
	return render_template('index.html',json_name=json_name)

@app.route('/files/<filename>')
def file(filename):
	path_file='/home/shiyanlou/files/'
	if os.path.isfile(path_file+filename+'.json'):
		with open(path_file+filename+'.json') as json_file:
				json_data=json.load(json_file)
				json_content=json_data.get('content')
	else:
		abort(404)
	return render_template('file.html',json_content=json_content)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

if __name__=='__main__':
	app.run()