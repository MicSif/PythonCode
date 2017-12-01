#!/usr/bin/env python3
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'
db = SQLAlchemy(app)
class File(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(80))
	created_time=db.Column(db.DateTime)
	category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
	content=db.Column(db.Text)
	category = db.relationship('Category',
        backref=db.backref('files', lazy='dynamic'))
	def __init__(self,title,created_time,category_id,content):
		self.title=title
		self.created_time=created_time
		self.category_id=category_id
		self.content=content
	def __repr__(self):
		return '<File %r>' % self.title
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Category %r>' % self.name

@app.route('/')
def index():
	files = File.query.all()
	file_title=[]
	if files:
		return render_template('index.html',file_name=files)
	else:
		abort(404)

@app.route('/files/<file_id>')
def file(file_id):
	file_list=[]
	choosen_file=File.query.filter_by(id=file_id).first()
	if choosen_file:
		cate=Category.query.filter_by(id=file_id).first().name
		file_list.append(choosen_file.content)
		file_list.append(choosen_file.created_time)
		file_list.append(cate)
	else:
		abort(404)
	return render_template('file.html',file_list=file_list)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'),404

if __name__=='__main__':
	app.run()