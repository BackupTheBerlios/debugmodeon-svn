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

from handlers.AuthenticatedHandler import *

class AdminUsers(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		self.values['tab'] = '/admin'
		
		if user.rol != 'admin':
			self.forbidden()
			return
		
		if method == 'GET':
			self.render('templates/admin-users.html')
		else:
			nickname = self.get_param('nickname')
			if nickname is None or nickname == '':
				self.values['m'] = u'Debes completar el campo nickname'
				self.render('/admin-users.html')
				return
			u = model.UserData.all().filter('nickname', nickname).get()
			if u is None:
				self.values['m'] = u'No existe el usuario %s' % (nickname)
				self.render('/admin-users.html')
				return
			action = self.get_param('action')
			if action == 'block_user':
				u.banned_date = datetime.datetime.now()
				u.put()
				self.values['m'] = u'El usuario %s ha sido baneado' % (nickname)
			elif action == 'unblock_user':
				u.banned_date = None
				u.put()
				self.values['m'] = u'El usuario %s ha sido desbaneado' % (nickname)
			else:
				self.values['m'] = u'No existe la acción %s' % (action)
			self.render('/admin-users.html')