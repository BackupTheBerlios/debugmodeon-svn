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

import re
import model

from img import *
from utilities import session
from google.appengine.ext import webapp
from google.appengine.ext import db
from handlers.AuthenticatedHandler import *
from google.appengine.ext.webapp import template

class UserChangePassword(AuthenticatedHandler):

	def execute(self):
		method = self.request.method

		if method == 'GET':
			self.values['redirect_to'] = self.request.get('redirect_to')
			self.render('templates/user-changepassword.html')
		else:
			old_password = self.request.get('old_password')
			password = self.request.get('password')

			if not password or len(password) < 4:
				self.error('La contraseña debe ser de al menos cuatro caracteres')
				return
			
			user = self.values['user']
			
			if self.hash(user.nickname, old_password) == user.password:
				user.password = self.hash(user.nickname, password)
				user.put()
				rt = self.request.get('redirect_to')
				if not rt:
					rt = '/'
				self.redirect(rt)
			else:
				self.error('Contraseña actual incorrecta')
				return

	def error(self, error):
		self.values['error'] = error
		self.render('templates/user-changepassword.html')