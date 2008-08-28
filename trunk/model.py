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

class Group(search.SearchableModel):
	owner = db.UserProperty(required=True)
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
	user = db.UserProperty(required=True)
	group = db.ReferenceProperty(Group,required=True)

class GroupItem(db.Model):
	user = db.UserProperty(required=True)
	item = db.ReferenceProperty(Group,required=True)

class Thread(db.Model):
	group = db.ReferenceProperty(Group,required=True)
	author = db.UserProperty(required=True)
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
	author = db.UserProperty(required=True)
	content = db.TextProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()