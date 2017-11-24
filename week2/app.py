#!/usr/bin/env python3
from flask import Flask,render_template,abort
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/news'
db = SQLAlchemy(app)
mongo_client = MongoClient('127.0.0.1', 27017)
mongo_db = mongo_client.news
class File(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	title=db.Column(db.String(80))
	created_time=db.Column(db.DateTime)
	category_id=db.Column(db.Integer,db.ForeignKey('category.id'))
	content=db.Column(db.Text)
	category=db.relationship('Category')
	def __init__(self,title,created_time,category_id,content):
		self.title=title
		self.created_time=created_time
		self.category_id=category_id
		self.content=content
	def __repr__(self):
		return '<File %r>' % self.title
	def add_tag(self, tag_name):
		if mongo_db.tags.find_one({'title':self.title,'tag':tag_name}) == None:
			mongo_db.tags.insert_one({'title':self.title,'tag':tag_name })
		else:
			pass
	def remove_tag(self,tag_name):
		mongo_db.tags.delete_one({'title':self.title,'tag':tag_name})
	@property
	def tags(self):
		tag_list=[]
		article=mongo_db.tags.find({'title':self.title})
		for each_tag in article:
			tag_list.append(each_tag['tag'])
		return tag_list 

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
	article_dict={}
	if files:
		for each_file in files:
			article_tags_list=[]
			article_title=each_file.title
			article_tags=mongo_db.tags.find({'title':article_title})
			for article_tag in article_tags:
				article_tags_list.append(article_tag['tag'])
			article_dict[article_title] = article_tags_list
		return render_template('index.html',file_name=files,tags_dict=article_dict)
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