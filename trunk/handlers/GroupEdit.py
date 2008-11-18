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
from google.appengine.api import memcache
from handlers.AuthenticatedHandler import *

class GroupEdit(AuthenticatedHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')

		if method == 'GET':
			if key:
				# show edit form
				group = model.Group.get(key)
				if user.nickname != group.owner.nickname and user.rol != 'admin':
					self.forbidden()
					return
				self.values['key'] = key

				self.values['title'] = group.title
				self.values['description'] = group.description
				if group.all_users is not None:
					self.values['all_users'] = group.all_users
				else:
					self.values['all_users'] = True
				if group.category:
					self.values['category'] = group.category
				self.add_categories()
				self.render('templates/group-edit.html')
			else:
				# show an empty form
				self.values['title'] = 'Grupo...'
				self.values['all_users'] = True
				self.add_categories()
				self.render('templates/group-edit.html')
		else:
			if key:
				# update group
				group = model.Group.get(key)
				if user.nickname != group.owner.nickname and user.rol != 'admin':
					self.forbidden()
					return
				# group title is not editable since many-to-many relationships are denormalizated
				# group.title = self.get_param('title')
				group.description = self.get_param('description')
				image = self.request.get("img")
				if image:
					image = images.im_feeling_lucky(image, images.JPEG)
					group.avatar = img.resize(image, 128, 128)
					group.thumbnail = img.resize(image, 48, 48)
					if not group.image_version:
						group.image_version = 1
					else:
						memcache.delete('/images/group/avatar/%s/%d' % (group.key().id(), group.image_version))
						memcache.delete('/images/group/thumbnail/%s/%d' % (group.key().id(), group.image_version))
						group.image_version += 1
					memcache.delete('/images/group/avatar/%s' % group.key().id())
					memcache.delete('/images/group/thumbnail/%s' % group.key().id())
				if self.get_param('all_users'):
					group.all_users = True
				else:
					group.all_users = False
				category = model.Category.get(self.request.get('category'))
				prev_category = group.category
				group.category = category
				group.put()
				
				if prev_category:
					prev_category.groups -= 1
					prev_category.put()
				
				category.groups += 1
				category.put()
				
				memcache.delete('index_groups')
				self.redirect('/group/%s' % (group.url_path, ))
			else:
				# new group
				title = self.get_param('title')
				url_path = '-'
				all_users = False
				if self.get_param('all_users'):
					all_users = True
				group = model.Group(owner=user,
					owner_nickname=user.nickname,
					title=title,
					description=self.get_param('description'),
					url_path=url_path,
					members=1,
					all_users = all_users,
					items=0,
					threads=0,
					responses=0,
					subscribers=[user.email],
					activity=1)
				category = model.Category.get(self.request.get('category'))
				group.category = category
				image = self.request.get("img")
				if image:
					image = images.im_feeling_lucky(image, images.JPEG)
					group.avatar = img.resize(image, 128, 128)
					group.thumbnail = img.resize(image, 48, 48)
					group.image_version = 1
				
				group.put()
				self.add_user_subscription(user, 'group', group.key().id())
				group.url_path = '%d/%s' % (group.key().id(), self.to_url_path(group.title))
				group.put()
				
				category.groups += 1
				category.put()
				
				user.groups += 1
				user.put()

				app = model.Application.all().get()
				if app:
					app.groups += 1
					app.put()
				memcache.delete('app')
				
				group_user = model.GroupUser(user=user,
					group=group,
					user_nickname=user.nickname,
					group_title=group.title,
					group_url_path=group.url_path)
				group_user.put()
				memcache.delete('index_groups')
				
				followers = list(self.get_followers(user=user))
				followers.append(user.nickname)
				self.create_event(event_type='group.new', followers=followers, user=user, group=group)
				
				self.add_follower('group', group.key().id(), user.nickname)
				
				# TODO: update a user counter to know how many groups is owner of?
				

				self.redirect('/group/%s' % (group.url_path, ))