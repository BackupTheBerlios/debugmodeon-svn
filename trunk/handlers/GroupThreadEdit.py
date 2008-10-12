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
				if user.rol != 'admin':
					if not self.can_update(thread.creation_date):
						self.error('No es posible editar pasados m&aacute;s de 15 minutos.')
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
					if not self.can_update(thread.creation_date):
						self.error('No es posible editar pasados m&aacute;s de 15 minutos.')
						return
				if thread.parent_thread is None:
					thread.title = self.get_param('title')
				thread.content = self.get_param('content')
				thread.put()
				self.redirect('/group.forum/%s' % (thread.url_path))
			else:
				self.error('Comentario no encontrado')
				return