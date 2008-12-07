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
import random

from img import *
from utilities import session
from handlers.BaseHandler import *

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext.webapp import template

class UserResetPassword(BaseHandler):

	def execute(self):
		method = self.request.method

		if method == 'GET':
			nickname = self.request.get('nickname')
			token = self.request.get('token')
			u = model.UserData.all().filter('nickname =', nickname).filter('token =', token).get()
			if not u:
				self.render('templates/user-resetpassword-error.html')
			else:
				self.values['token'] = token
				self.values['nickname'] = nickname
				self.render('templates/user-resetpassword.html')
		elif self.auth():
			token = self.request.get('token')
			nickname = self.request.get('nickname')
			password = self.request.get('password')
			re_password = self.request.get('re_password')
			
			if not password or len(password) < 4:
				self.show_error(nickname, token, 'La contraseña debe ser de al menos cuatro caracteres')
				return

			if password != re_password:
				self.show_error(nickname, token, 'La nueva contraseña y la nueva contraseña repetida no son iguales')
				return
			
			u = model.UserData.all().filter('nickname =', nickname).filter('token =', token).get()
			if not u:
				self.render('templates/user-resetpassword-error.html')
				return
			
			u.token = None
			u.password = self.hash_password(nickname, password)
			u.put()
			self.render('templates/user-resetpassword-login.html')

	def show_error(self, nickname, token, error):
		self.values['nickname'] = nickname
		self.values['token'] = token
		self.values['error'] = error
		self.render('templates/user-resetpassword.html')