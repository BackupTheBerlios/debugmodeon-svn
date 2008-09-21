#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte at gmail dot com>
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
from handlers.AuthenticatedHandler import *

class GroupForumView(BaseHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		user = self.values['user']
		url_path = self.request.path.split('/', 2)[2]
		thread = model.Thread.gql('WHERE url_path=:1', url_path).get()
		if not thread:
			self.not_found()
			return
		group = thread.group

		self.values['group'] = group
		self.values['joined'] = self.joined(group)
		self.values['thread'] = thread
		query = model.ThreadResponse.all().filter('thread =', thread).order('creation_date')
		self.values['responses'] = self.paging(query, 10)
		
		if user:
			if user.email in thread.subscribers:
				self.values['cansubscribe']=False
			else:
				self.values['cansubscribe']=True

		self.render('templates/group-forum-view.html')
