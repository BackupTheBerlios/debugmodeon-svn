#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# 
# This file is part of "debug_mode_on".
# 
# "debug_mode_on" is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# "debug_mode_on" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with "debug_mode_on".  If not, see <http://www.gnu.org/licenses/>.
# 

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import search

class UserData(db.Model):
	nickname = db.StringProperty(required=True)
	email = db.StringProperty(required=True)
	avatar = db.BlobProperty()
	thumbnail = db.BlobProperty()
	
	password = db.StringProperty(required=True)
	rol = db.StringProperty()
	google_adsense = db.StringProperty()
	google_adsense_channel = db.StringProperty()
	token = db.StringProperty()
	checked = db.BooleanProperty()
	
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
	rating_average = db.IntegerProperty(required=True)
	# forums
	threads = db.IntegerProperty(required=True)
	responses = db.IntegerProperty(required=True)
	# groups
	groups = db.IntegerProperty(required=True)
	# favourites
	favourites = db.IntegerProperty(required=True)
	# others
	country = db.StringProperty()
	city = db.StringProperty()
	public = db.BooleanProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Item(search.SearchableModel):
	author = db.ReferenceProperty(UserData,required=True)
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	lic = db.StringProperty(required=True)
	views = db.IntegerProperty(required=True)
	rating_count = db.IntegerProperty(required=True)
	rating_total = db.IntegerProperty(required=True)
	rating_average = db.IntegerProperty()
	url_path = db.StringProperty(required=True)
	responses = db.IntegerProperty(required=True)
	tags = db.StringListProperty()
	favourites = db.IntegerProperty(required=True)
	
	draft = db.BooleanProperty(required=True)
	item_type = db.StringProperty(required=True)
	subscribers = db.StringListProperty()
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Comment(db.Model):
	content = db.TextProperty(required=True)
	item = db.ReferenceProperty(Item,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Vote(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	item = db.ReferenceProperty(Item,required=True)
	rating = db.IntegerProperty(required=True)

class Tag(db.Model):
	tag = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True)

class Group(search.SearchableModel):
	owner = db.ReferenceProperty(UserData,required=True)
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	url_path = db.StringProperty(required=True)
	
	members = db.IntegerProperty(required=True)
	items = db.IntegerProperty(required=True)
	threads = db.IntegerProperty(required=True)
	responses = db.IntegerProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class GroupUser(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	group = db.ReferenceProperty(Group,required=True)

class GroupItem(db.Model):
	item = db.ReferenceProperty(Item,required=True)
	group = db.ReferenceProperty(Group,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)

class Thread(db.Model):
	group = db.ReferenceProperty(Group,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	title = db.StringProperty(required=True)
	url_path = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	
	responses = db.IntegerProperty(required=True)
	latest_response = db.DateTimeProperty()

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class ThreadResponse(db.Model):
	thread = db.ReferenceProperty(Thread,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	content = db.TextProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Favourite(db.Model):
	item=db.ReferenceProperty(Item,required=True)
	user=db.ReferenceProperty(UserData,required=True)
	
