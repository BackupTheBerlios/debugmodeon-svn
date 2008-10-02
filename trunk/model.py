#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# (C) Copyright 2008 Ignacio Andreu <plunchete at gmail dot com>
# (C) Copyright 2008 Néstor Salceda <nestor.salceda at gmail dot com>
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
	
class UserData(search.SearchableModel):
	nickname = db.StringProperty(required=True)
	personal_message = db.StringProperty()
	email = db.StringProperty(required=True)
	avatar = db.BlobProperty()
	thumbnail = db.BlobProperty()
	image_version = db.IntegerProperty()
	list_urls = db.StringListProperty()
	im_addresses = db.StringListProperty()
	about_user = db.TextProperty()
	
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
	real_name = db.StringProperty()
	country = db.StringProperty()
	city = db.StringProperty()
	public = db.BooleanProperty(required=True)
	contacts = db.IntegerProperty()

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()
	last_login = db.DateTimeProperty()

class ItemHtml(db.Model):
	content = db.TextProperty(required=True)

class Item(search.SearchableModel):
	author = db.ReferenceProperty(UserData,required=True)
	author_nickname = db.StringProperty()
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	content_html = db.ReferenceProperty(ItemHtml)
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
	deletion_message = db.StringProperty()
	deletion_user = db.ReferenceProperty(UserData,collection_name='du')

class Comment(db.Model):
	content = db.TextProperty(required=True)
	item = db.ReferenceProperty(Item,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	author_nickname = db.StringProperty()
	response_number = db.IntegerProperty()
	
	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()
	deletion_message = db.StringProperty()

class Vote(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	item = db.ReferenceProperty(Item,required=True)
	rating = db.IntegerProperty(required=True)

class Tag(db.Model):
	tag = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True)

class Group(search.SearchableModel):
	owner = db.ReferenceProperty(UserData,required=True)
	owner_nickname = db.StringProperty()
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	url_path = db.StringProperty(required=True)
	subscribers = db.StringListProperty()
	
	members = db.IntegerProperty(required=True)
	items = db.IntegerProperty(required=True)
	threads = db.IntegerProperty(required=True)
	responses = db.IntegerProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()
	
	avatar = db.BlobProperty()
	thumbnail = db.BlobProperty()
	image_version = db.IntegerProperty()
	
	all_users = db.BooleanProperty()

class GroupUser(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	group = db.ReferenceProperty(Group,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)

class GroupItem(db.Model):
	item = db.ReferenceProperty(Item,required=True)
	group = db.ReferenceProperty(Group,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)

class Thread(search.SearchableModel):
	group = db.ReferenceProperty(Group,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	author_nickname = db.StringProperty()
	title = db.StringProperty(required=True)
	url_path = db.StringProperty()
	content = db.TextProperty(required=True)
	subscribers = db.StringListProperty()
	
	last_response_date = db.DateTimeProperty()
	response_number = db.IntegerProperty()
	
	# responses
	parent_thread = db.SelfReferenceProperty()
	
	responses = db.IntegerProperty(required=True)
	latest_response = db.DateTimeProperty()

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()
	
	deletion_message = db.StringProperty()

class ThreadResponse(db.Model):
	thread = db.ReferenceProperty(Thread,required=True)
	author = db.ReferenceProperty(UserData,required=True)
	content = db.TextProperty(required=True)

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()

class Favourite(db.Model):
	item = db.ReferenceProperty(Item,required=True)
	user = db.ReferenceProperty(UserData,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	
class Contact(db.Model):
	user_from = db.ReferenceProperty(UserData,required=True,collection_name='cf')
	user_to = db.ReferenceProperty(UserData,required=True,collection_name='ct')
	creation_date = db.DateTimeProperty(auto_now_add=True)

class Application(db.Model):
	users = db.IntegerProperty()
	groups = db.IntegerProperty()
	items = db.IntegerProperty()
	threads = db.IntegerProperty()
	
	url = db.StringProperty()
	
	mail_subject_prefix = db.StringProperty()
	mail_sender = db.StringProperty()
	mail_footer = db.StringProperty()
	
	recaptcha_public_key = db.StringProperty()
	recaptcha_private_key = db.StringProperty()
	
	google_adsense = db.StringProperty()
	google_adsense_channel = db.StringProperty()