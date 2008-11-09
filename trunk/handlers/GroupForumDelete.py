#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Ignacio Andreu <plunchete at gmail dot com>
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

import datetime

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class GroupForumDelete(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		if user.rol != 'admin':
			self.forbidden()
			return
		thread = model.Thread.get(self.get_param('key'))
		url = '/group.forum.list/' + thread.group.url_path
		if not thread:
			self.not_found()
			return
		if thread.parent_thread is not None:
			message = self.get_param('message')
			#decrement number of childs in the parent thread
			thread.parent_thread.put()
			#Delete child thread
			thread.deletion_date = datetime.datetime.now()
			thread.deletion_message = message
			thread.put()
		else:
			#decrement threads in the group
			group = thread.group
			if group.activity:
				value = 5 + (2 * thread.responses)
				group.activity -= value
			group.threads -=1
			group.put()
			#decrement thread in the app
			app = model.Application().all().get()
			app.threads -= 1
			app.put()
			memcache.delete('app')
			#delete comments in this thread
			childs = model.Thread.all().filter('parent_thread', thread)
			db.delete(childs)
			memcache.delete('index_threads')
			thread.delete()

		self.redirect(url)
