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
			# TODO: try with the id in the url_path and redirect
			self.not_found()
			return
		
		if len(thread.url_path.split('/')) == 2:
			responses = model.ThreadResponse.all().filter('thread', thread).order('creation_date')
			for r in responses:
				resp = model.Thread(group=thread.group,
					author=r.author,
					title=thread.title,
					url_path=None,
					content=r.content,
					parent_thread=thread,
					responses=0,
					last_update=r.last_update,
					creation_date=r.creation_date,
					deletion_date=r.deletion_date)
				resp.put()
				r.delete()
			thread.url_path = '%d/%s' % (thread.key().id(), thread.url_path)
			thread.parent_thread = None
			thread.put()
			self.redirect('/group.forum/%s' % thread.url_path)
			return
				
		group = thread.group

		self.values['group'] = group
		self.values['joined'] = self.joined(group)
		self.values['thread'] = thread
		query = model.Thread.all().filter('parent_thread', thread).order('creation_date')
		self.values['responses'] = self.paging(query, 10)
		
		if user:
			if user.email in thread.subscribers:
				self.values['cansubscribe']=False
			else:
				self.values['cansubscribe']=True

		self.render('templates/group-forum-view.html')
