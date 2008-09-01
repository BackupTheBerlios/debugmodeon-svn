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

from handlers.BaseHandler import *
from google.appengine.api import users

class UserList(BaseHandler):

	def execute(self):
		self.values['tab'] = '/user.list'
		query = model.UserData.all().filter('public =', True).order('-creation_date')
		us = self.paging(query, 10)
		"""
		for user in us:
			u = users.User(user.email)
			threads = model.Thread.all().filter('author =', u).count(1000)
			responses = model.ThreadResponse.all().filter('author =', u).count(1000)
			groups = model.GroupUser.all().filter('user =', u).count(1000)
			
			if threads > 0 or responses > 0 or groups > 0:
				user.public = True
			else:
				user.public = False
			user.threads = threads
			user.responses = responses
			user.groups = groups
			user.put()
		"""
		self.values['users'] = us
		self.render('templates/user-list.html')
