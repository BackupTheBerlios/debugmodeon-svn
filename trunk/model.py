#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import search

class Item(search.SearchableModel):
	author = db.UserProperty(required=True)
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	lic = db.StringProperty(required=True)
	views = db.IntegerProperty(required=True)
	rating_count = db.IntegerProperty(required=True)
	rating_total = db.IntegerProperty(required=True)
	url_path = db.StringProperty(required=True)
	responses = db.IntegerProperty(required=True)
	tags = db.StringListProperty()
	
	draft = db.BooleanProperty(required=True)
	item_type = db.StringProperty(required=True)
	subscribers = db.StringListProperty()
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Comment(db.Model):
	content = db.TextProperty(required=True)
	item = db.ReferenceProperty(Item,required=True)
	author = db.UserProperty(required=True)
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Vote(db.Model):
	user = db.UserProperty(required=True)
	item = db.ReferenceProperty(Item,required=True)
	vote = db.BooleanProperty(required=True)

class Tag(db.Model):
	tag = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True)

class UserData(db.Model):
	nickname = db.StringProperty(required=True)
	email = db.StringProperty(required=True)
	avatar = db.BlobProperty()
	thumbnail = db.BlobProperty()
	# items
	items = db.IntegerProperty(required=True)
	draft_items = db.IntegerProperty(required=True)
	# messages
	messages = db.IntegerProperty(required=True)
	draft_messages = db.IntegerProperty(required=True)
	# comments
	comments = db.IntegerProperty(required=True)
	# rating
	rating_count = db.IntegerProperty(required=True)
	rating_total = db.IntegerProperty(required=True)
	# others
	country = db.StringProperty()
	city = db.StringProperty()
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

