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

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class GroupThreadEdit(AuthenticatedHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')

		if method == 'GET':
			if key:
				# show edit form
				thread = model.Thread.get(key)
				if user.nickname!= thread.author_nickname and user.rol != 'admin':
					self.forbidden()
					return
				if thread is None:
					self.not_found()
					return
				#TODO Check if it's possible
				if thread.parent_thread is None:
					self.values['is_parent_thread'] = True
				self.values['thread'] = thread
				self.render('templates/group-thread-edit.html')
				return
			else:
				self.error('Hilo no encontrado')
				return
		else:
			if key:
				# update comment
				thread = model.Thread.get(key)
				if user.nickname!= thread.author_nickname and user.rol != 'admin':
					self.forbidden()
					return
				if thread is None:
					self.not_found()
					return
				if user.rol != 'admin':
					if thread.editions is None:
						thread.editions = 0
					thread.editions +=1
					thread.last_edition = datetime.datetime.now()
				if thread.parent_thread is None:
					if thread.responses <= 5:
						thread.title = self.get_param('title')
						for comment in model.Thread.all().filter('parent_thread', thread):
							comment.title = thread.title
							comment.put()
				thread.content = self.get_param('content')
				thread.put()
				if thread.parent_thread is None:
					self.redirect('/group.forum/%s' % (thread.url_path))
				else:
					results = 20
					app = self.get_application()
					if app.max_results_sublist:
						results = app.max_results_sublist
					page = thread.response_number / results
					if (thread.response_number % results) > 0:
						page += 1
					self.redirect('/group.forum/%s?p=%d#comment-%s' % (thread.url_path, page, thread.response_number))
			else:
				self.error('Comentario no encontrado')
				return