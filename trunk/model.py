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
	unread_messages = db.IntegerProperty()
	sent_messages = db.IntegerProperty()
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
	banned_date = db.DateTimeProperty()

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
	editions = db.IntegerProperty()
	last_edition = db.DateTimeProperty()

class Vote(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	item = db.ReferenceProperty(Item,required=True)
	rating = db.IntegerProperty(required=True)

class Tag(db.Model):
	tag = db.StringProperty(required=True)
	count = db.IntegerProperty(required=True)
	
class Category(db.Model):
	parent_category = db.SelfReferenceProperty()
	title = db.StringProperty(required=True)
	url_path = db.StringProperty()
	description = db.StringProperty(required=True)
	groups = db.IntegerProperty(required=True)
	items = db.IntegerProperty(required=True)
	
	subcategories = None

class Group(search.SearchableModel):
	owner = db.ReferenceProperty(UserData,required=True)
	owner_nickname = db.StringProperty()
	title = db.StringProperty(required=True)
	description = db.StringProperty(required=True)
	url_path = db.StringProperty(required=True)
	old_url_path = db.StringProperty()
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
	
	category = db.ReferenceProperty(Category, collection_name='groups_set')
	
	activity = db.IntegerProperty()

class GroupUser(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	group = db.ReferenceProperty(Group,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	# denormalization
	user_nickname = db.StringProperty()
	group_title = db.StringProperty()
	group_url_path = db.StringProperty()

class GroupItem(db.Model):
	item = db.ReferenceProperty(Item,required=True)
	group = db.ReferenceProperty(Group,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	# denormalization
	item_author_nickname = db.StringProperty()
	item_title = db.StringProperty()
	item_url_path = db.StringProperty()
	group_title = db.StringProperty()
	group_url_path = db.StringProperty()
	

class Thread(search.SearchableModel):
	group = db.ReferenceProperty(Group,required=True)
	group_title = db.StringProperty()
	group_url_path = db.StringProperty()
	author = db.ReferenceProperty(UserData,required=True)
	author_nickname = db.StringProperty()
	title = db.StringProperty(required=True)
	url_path = db.StringProperty()
	content = db.TextProperty(required=True)
	subscribers = db.StringListProperty()
	
	last_response_date = db.DateTimeProperty()
	response_number = db.IntegerProperty()
	
	editions = db.IntegerProperty()
	last_edition = db.DateTimeProperty()
	
	# responses
	parent_thread = db.SelfReferenceProperty()
	
	responses = db.IntegerProperty(required=True)
	latest_response = db.DateTimeProperty()

	last_update = db.DateTimeProperty(auto_now=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	deletion_date = db.DateTimeProperty()
	
	deletion_message = db.StringProperty()
	views = db.IntegerProperty()

class Favourite(db.Model):
	item = db.ReferenceProperty(Item,required=True)
	user = db.ReferenceProperty(UserData,required=True)
	creation_date = db.DateTimeProperty(auto_now_add=True)
	# denormalize
	item_author_nickname = db.StringProperty()
	item_title = db.StringProperty()
	item_url_path = db.StringProperty()
	user_nickname = db.StringProperty()
	
class Contact(db.Model):
	user_from = db.ReferenceProperty(UserData,required=True,collection_name='cf')
	user_to = db.ReferenceProperty(UserData,required=True,collection_name='ct')
	creation_date = db.DateTimeProperty(auto_now_add=True)
	# denormalize
	user_from_nickname = db.StringProperty()
	user_to_nickname = db.StringProperty()

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
	
	max_results = db.IntegerProperty()
	max_results_sublist = db.IntegerProperty()
	
class Message(db.Model):
	user_from = db.ReferenceProperty(UserData,required=True,collection_name='mf')
	user_to = db.ReferenceProperty(UserData,required=True,collection_name='mt')
	creation_date = db.DateTimeProperty(auto_now_add=True)
	title = db.StringProperty(required=True)
	url_path = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	read = db.BooleanProperty(required=True)
	from_deletion_date = db.DateTimeProperty()
	to_deletion_date = db.DateTimeProperty()

	user_from_nickname = db.StringProperty()
	user_to_nickname = db.StringProperty()

class RelatedGroup(db.Model):
	group_from = db.ReferenceProperty(Group,required=True,collection_name='gf')
	group_to = db.ReferenceProperty(Group,required=True,collection_name='gt')
	creation_date = db.DateTimeProperty(auto_now_add=True)
	# denormalization
	group_from_title = db.StringProperty(required=True)
	group_from_url_path = db.StringProperty(required=True)
	group_to_title = db.StringProperty(required=True)
	group_to_url_path = db.StringProperty(required=True)
	
class UserSubscription(db.Model):
	user = db.ReferenceProperty(UserData,required=True)
	user_email = db.StringProperty(required=True)
	user_nickname = db.StringProperty(required=True)
	subscription_type = db.StringProperty(required=True)
	subscription_id = db.IntegerProperty(required=True)
	creation_date = db.DateTimeProperty()
	
class Follower(db.Model):
	object_type = db.StringProperty(required=True)
	object_id = db.IntegerProperty(required=True)
	followers = db.StringListProperty()

"""
class Event(db.Model):
	event_type = db.StringProperty(required=True)
	followers = db.StringListProperty(required=True)
	
	user = db.ReferenceProperty(UserData,required=True)
	user_nickname = db.StringProperty(required=True)
	
	user_to = db.ReferenceProperty(UserData,required=True)
	user_to_nickname = db.StringProperty(required=True)
	
	group = db.ReferenceProperty(Group)
	group_title = db.StringProperty()
	group_url_path = db.StringProperty()
	
	item = db.ReferenceProperty(Item)
	item_author_nickname = db.StringProperty()
	item_title = db.StringProperty()
	item_url_path = db.StringProperty()
	
	thread = db.ReferenceProperty(Thread)
	thread_title = db.StringProperty(required=True)
	thread_url_path = db.StringProperty()
"""