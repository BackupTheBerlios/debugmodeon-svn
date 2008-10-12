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

class GroupForumMove(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		if user.rol != 'admin':
			self.forbidden()
			return
			
		if method == 'GET':
			thread_key = self.get_param('thread_key')
			
			thread = model.Thread.get(thread_key)
			if thread is None:
				self.not_found()
				return
			
			self.values['thread_key'] = thread.key
			self.render('templates/group-forum-move.html')
			return
		else:
			thread_key = self.get_param('thread_key')
			group_key = self.get_param('group_key')
			thread = model.Thread.get(thread_key)
			group = model.Group.get(group_key)
			if group is None or thread is None:
				self.values['thread_key'] = thread.key
				self.values['message'] = 'Grupo inexistente.'
				self.render('templates/group-forum-move.html')
				return
			
			if group.title == thread.group.title:
				self.values['thread_key'] = thread.key
				self.values['message'] = 'El grupo en el que est&aacute; el hilo y al que queires mover es el mismo, no entiendo qu&eacute; quieres hacer.'
				self.render('templates/group-forum-move.html')
				return
			#decrement threads in previous group
			group_orig = thread.group
			group_orig.threads -= 1
			
			#change gorup in thread and desnormalizated fields
			thread.group = group
			thread.group_title = group.title
			thread.group_url_path = group.url_path
			
			#increment threads in actual group
			group.threads += 1

			#update comments
			responses = model.Thread.all().filter('parent_thread', thread)
			for response in responses:
				response.group = group
				response.group_title = group.title
				response.group_url_path = group.url_path
				response.put()
			
			#save fields
			group_orig.put()
			thread.put()
			group.put()
			
			
			self.redirect('/group.forum/%s' % (thread.url_path))
			return
			
