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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from handlers.BaseHandler import *

class Apocalipto(BaseHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		
		# self.create_task('delete_recommendations', 2, {'offset': 0})
		# self.response.out.write('Delete recommendations scheduled tasks have begun')
		# return
		
		app = model.Application.all().get()
		
		if app is None:
			app = model.Application()
			app.recaptcha_public_key = '6LdORAMAAAAAAL42zaVvAyYeoOowf4V85ETg0_h-'
			app.recaptcha_private_key = '6LdORAMAAAAAAGS9WvIBg5d7kwOBNaNpqwKXllMQ'
			app.users = 0
			app.groups = 0
			app.items = 0
			app.threads = 0
			app.url = "http://localhost:8080"
			app.mail_subject_prefix = "[localhost]"
			app.mail_sender = "admin@example.com"
			app.mail_footer = ""
			app.max_results = 20
			app.max_results_sublist = 20
			import sha, random
			app.session_seed = sha.new(str(random.random())).hexdigest()
			app.put()
			
			user = model.UserData(nickname='admin',
				email='admin@example.com',
				password='1:c07cbf8821d47575a471c1606a56b79e5f6e6a68',
				items=0,
				draft_items=0,
				messages=0,
				draft_messages=0,
				comments=0,
				rating_count=0,
				rating_total=0,
				rating_average=0,
				threads=0,
				responses=0,
				groups=0,
				favourites=0,
				public=False,
				contacts=0,
				rol='admin')
			user.put()
			
			parent_category = model.Category(title='Programacion',
			   description='description',
			   items = 0,
			   groups = 0)
			parent_category.put()
			
			category = model.Category(title='Lenguajes de programacion',
			   description='description',
			   items = 0,
			   groups = 0)
			
			category.parent_category = parent_category
			category.put()
			
			self.response.out.write('App installed. Created user administrator. nickname="admin", password="1234". Please change the password.')
			return
		elif not app.session_seed:	
			import sha, random
			app.session_seed = sha.new(str(random.random())).hexdigest()
			app.put()
			self.response.out.write('Seed installed')
		
		return
		
		p = int(self.request.get('p'))
		key = self.request.get('key')
		action = self.request.get('action')
		if key:
			group = model.Group.get(key)
			if not group:
				self.response.out.write('group not found')
				return
		
		offset = (p-1)*10
		if action == 'gi':
			i = self.group_items(group, offset)
		elif action == 'gu':
			i = self.group_users(group, offset)
		elif action == 'th':
			i = self.threads(offset)
		elif action == 'cc':
			i = self.contacts(offset)
		elif action == 'fv':
			i = self.favourites(offset)
		elif action == 'sg':
			i = self.show_groups(offset)
			return
		elif action == 'ut':
			i = self.update_threads(offset)
		elif action == 'uis':
			i = self.update_item_subscription(p-1)
			self.response.out.write('Processed from %d to %d. %d updated. Action %s' % (p-1, i[0], i[1], action))
			return
		elif action == 'ugs':
			i = self.update_group_subscription(group, offset)
		elif action == 'uts':
			i = self.update_thread_subscription(p-1)
			self.response.out.write('Processed from %d to %d. %d updated. Action %s' % (p-1, i[0], i[1], action))
			return
		elif action == 'ugc':
			i = self.update_group_counters(p-1)
			self.response.out.write('Processed from %d to %d. %d updated. Action %s' % (p-1, i[0], i[1], action))
			return
		elif action == 'adus':
			i = self.add_date_user_subscription(offset)
		elif action == 'afg':
			i = self.add_follower_group(offset)
		elif action == 'afu':
			i = self.add_follower_user(offset)
		elif action == 'afi':
			i = self.add_follower_item(offset)
		elif action == 'aft':
			i = self.add_follower_thread(offset)
		else:
			self.response.out.write('unknown action -%s-' % action)
			return
		self.response.out.write('Processed from %d to %d. %d updated. Action %s' % (offset, i[0], i[1], action))

	def group_items(self, group, offset):
		i = offset
		p = 0
		for gi in model.GroupItem.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not gi.group_title:
				item = gi.item
				group = gi.group
				gi.item_author_nickname = item.author_nickname
				gi.item_title = item.title
				gi.item_url_path = item.url_path
				gi.group_title = group.title
				gi.group_url_path = group.url_path
				gi.put()
				p += 1
			i+=1
		return (i, p)

	def group_users(self, group, offset):
		i = offset
		p = 0
		for gu in model.GroupUser.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not gu.group_title:
				user = gu.user
				group = gu.group
				gu.user_nickname = gu.user.nickname
				gu.group_title = group.title
				gu.group_url_path = group.url_path
				gu.put()
				p += 1
			i+=1
		return (i, p)

	def threads(self, offset):
		i = offset
		p = 0
		for th in model.Thread.all().order('-creation_date').fetch(10, offset):
			if not th.group_title:
				group = th.group
				th.group_title = group.title
				th.group_url_path = group.url_path
				if not th.url_path:
					th.url_path = th.parent_thread.url_path
				th.put()
				p += 1
			i+=1
		return (i, p)

	def contacts(self, offset):
		i = offset
		p = 0
		for cc in model.Contact.all().order('-creation_date').fetch(10, offset):
			if not cc.user_from_nickname:
				cc.user_from_nickname = cc.user_from.nickname
				cc.user_to_nickname = cc.user_to.nickname
				cc.put()
				p += 1
			i+=1
		return (i, p)

	def favourites(self, offset):
		i = offset
		p = 0
		for fv in model.Favourite.all().order('-creation_date').fetch(10, offset):
			if not fv.user_nickname:
				item = fv.item
				fv.item_author_nickname = item.author_nickname
				fv.item_title = item.title
				fv.item_url_path = item.url_path
				fv.user_nickname = fv.user.nickname
				fv.put()
				p += 1
			i+=1
		return (i, p)

	def show_groups(self, offset):
		for g in model.Group.all().order('-creation_date').fetch(10, offset):
			self.response.out.write("('%s', '%s', %d),\n" % (g.title, str(g.key()), g.members))
			
	def update_threads(self, offset):
		i = offset
		p = 0
		for th in model.Thread.all().filter('parent_thread', None).order('-creation_date').fetch(10, offset):
			if th.views is None:
				th.views = 0
				th.put()
				p += 1
			i+=1
		return (i, p)
		
	def update_item_subscription(self, offset):
		i = offset
		p = 0
		for item in model.Item.all().order('-creation_date').fetch(1, offset):
			if item.subscribers:
				for subscriber in item.subscribers:
					user = model.UserData.all().filter('email', subscriber).get()
					if not model.UserSubscription.all().filter('user', user).filter('subscription_type', 'item').filter('subscription_id', item.key().id()).get():
						self.add_user_subscription(user, 'item', item.key().id())
						p += 1
			i+=1
		return (i, p)
		
	def update_group_subscription(self, group, offset):
		i = offset
		p = 0
		for group_user in model.GroupUser.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not model.UserSubscription.all().filter('user', group_user.user).filter('subscription_type', 'group').filter('subscription_id', group.key().id()).get():
				self.add_user_subscription(group_user.user, 'group', group.key().id())
				p += 1
			i += 1
		return (i, p)
			
	def update_thread_subscription(self, offset):
		i = offset
		p = 0
		for thread in model.Thread.all().filter('parent_thread', None).order('-creation_date').fetch(1, offset):
			if thread.subscribers:
				for subscriber in thread.subscribers:
					user = model.UserData.all().filter('email', subscriber).get()
					if not model.UserSubscription.all().filter('user', user).filter('subscription_type', 'thread').filter('subscription_id', thread.key().id()).get():
						self.add_user_subscription(user, 'thread', thread.key().id())
						p += 1
				i+=1
		return (i, p)
		
	def update_group_counters(self, offset):
		i = offset
		p = 0
		for group in model.Group.all().order('-creation_date').fetch(1, offset):
			users = model.GroupUser.all().filter('group', group).count()
			items = model.GroupItem.all().filter('group', group).count()
			group_threads = model.Thread.all().filter('group', group).filter('parent_thread', None)
			threads = group_threads.count()
			comments = 0
			for thread in group_threads:
				comments += model.Thread.all().filter('group', group).filter('parent_thread', thread).count()
			if group.members != users or group.items != items or group.threads != threads or group.responses != comments:
				group.members = users
				group.items = items
				group.threads = threads
				group.responses = comments
				p += 1
			if not group.activity:
				group.activity = 0
			group.activity = (group.members * 1) + (group.threads * 5) + (group.items * 15) + (group.responses * 2)
			group.put()
			i += 1
		return (i, p)
			
	def add_date_user_subscription(self, offset):
		i = offset
		p = 0
		for user_subscription in model.UserSubscription.all().fetch(10, offset):
			if user_subscription.creation_date is None:
				user_subscription.creation_date = datetime.datetime.now()
				user_subscription.put()
				p += 1
			i += 1
		return (i, p)
		
	def add_follower_group(self, offset):
		i = offset
		p = 0
		for group_user in model.GroupUser.all().fetch(10, offset):
			if group_user.user_nickname is None:
				self.desnormalizate_group_user(group_user)
			self.add_follower(group=group, nickname=group_user.user_nickname)
			p +=1
			i += 1
		return(i,p)
	
	def add_follower_user(self, offset):
		i = offset
		p = 0
		for cc in model.Contact.all().fetch(10, offset):
			if cc.user_from_nickname is None:
				self.desnormalizate_user_contact(cc)
			self.add_follower(user=cc.user_to, nickname=cc.user_from_nickname)
			p += 1
			i += 1
		return(i,p)
	
	def add_follower_item(self, offset):
		i = offset
		p = 0
		for item in model.Item.all().filter('deletion_date', None).filter('draft', False).fetch(10, offset):
			self.add_follower(item=item, nickname=item.author_nickname)
			p += 1
			i += 1
		return(i,p)
		
	def add_follower_thread(self, offset):
		i = offset
		p = 0
		for t in model.Thread.all().filter('parent_thread', None).fetch(10, offset):
			self.add_follower(thread=t, nickname=t.author_nickname)
			p += 1
			i += 1
		return(i, p)
		
	def desnormalizate_group_user(self, gu):
		user = gu.user
		group = gu.group
		gu.user_nickname = gu.user.nickname
		gu.group_title = group.title
		gu.group_url_path = group.url_path
		gu.put()
		
	def desnormalizate_user_contact(cc):
		cc.user_from_nickname = cc.user_from.nickname
		cc.user_to_nickname = cc.user_to.nickname
		cc.put()
		