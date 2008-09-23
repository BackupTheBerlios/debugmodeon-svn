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
from handlers.BaseHandler import *

class GroupForumList(BaseHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		url_path = self.request.path.split('/', 2)[2]
		group = model.Group.gql('WHERE url_path=:1', url_path).get()
		if not group:
			self.not_found()
			return

		self.values['group'] = group
		self.values['joined'] = self.joined(group)
		query = model.Thread.all().filter('group =', group).order('-last_update')
		threads = []
		for t in query:
			if t.url_path is not None:
				threads.append(t)
		self.values['threads'] = threads # self.paging(query, 10)
		self.render('templates/group-forum-list.html')