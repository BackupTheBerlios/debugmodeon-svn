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
				if user.nickname != group.owner.nickname:
					self.forbidden()
					return
				self.values['key'] = key

				self.values['title'] = group.title
				self.values['description'] = group.description
				if group.all_users is not None:
					self.values['all_users'] = group.all_users
				else:
					self.values['all_users'] = True
				self.render('templates/group-edit.html')
			else:
				# show an empty form
				self.values['title'] = 'Grupo...'
				self.values['all_users'] = True
				self.render('templates/group-edit.html')
		else:
			if key:
				# update group
				group = model.Group.get(key)
				if user.nickname != group.owner.nickname:
					self.forbidden()
					return
				group.title = self.get_param('title')
				group.description = self.get_param('description')
				image = self.request.get("img")
				if image:
					image = images.im_feeling_lucky(image, images.JPEG)
					group.avatar = img.resize(image, 128, 128)
					group.thumbnail = img.resize(image, 48, 48)
				if self.get_param('all_users'):
					group.all_users = True
				else:
					group.all_users = False
				group.put()
				memcache.delete('/images/group/avatar/%s' % group.key().id())
				memcache.delete('/images/group/thumbnail/%s' % group.key().id())
				memcache.delete('index_groups')
				self.redirect('/group/%s' % (group.url_path, ))
			else:
				# new group
				title = self.get_param('title')
				url_path = self.to_url_path(title)
				url_path = self.unique_url_path(model.Group, url_path)
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
					subscribers=[user.email])
				image = self.request.get("img")
				if image:
					image = images.im_feeling_lucky(image, images.JPEG)
					group.avatar = img.resize(image, 128, 128)
					group.thumbnail = img.resize(image, 48, 48)
				
				group.put()
				
				user.groups += 1
				user.put()

				app = self.get_application()
				if app:
					app.groups += 1
					app.put()
				
				group_user = model.GroupUser(user=user, group=group)
				group_user.put()
				memcache.delete('index_groups')

				# TODO: update a user counter to know how many groups is owner of?

				self.redirect('/group/%s' % (group.url_path, ))