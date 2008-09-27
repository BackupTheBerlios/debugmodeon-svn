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

import model
import datetime

from utilities import session
from handlers.BaseHandler import *

class UserLogin(BaseHandler):

	def execute(self):
		values = self.values
		session.Session().delete()

		method = self.request.method

		if method == 'GET':
			self.values['redirect_to'] = self.request.get('redirect_to')
			self.render('templates/user-login.html')
		else:
			nickname = self.request.get('nickname')
			password = self.request.get('password')		

			user = model.UserData.gql('WHERE nickname=:1', nickname).get()
			if user:
				
				if self.check_password(user, password):
					values['user'] = user
					user.last_login = datetime.datetime.now()
					user.put()
					self.sess = session.Session()
					self.sess['user_nickname'] = user.nickname
					self.sess['user_email'] = user.email
					if user.rol:
						self.sess['user_rol'] = user.rol
					self.sess['user_key'] = user.key()
					self.sess['user'] = user
					rt = self.request.get('redirect_to')
					if rt:
						self.redirect(rt)
					else:
						self.redirect('/')
				else:
					self.show_error(nickname, u'Usuario o contraseña incorrectos')
			else:
				self.show_error(nickname, u'Usuario o contraseña incorrectos')
	
	def show_error(self, nickname, error):
		self.values['nickname'] = nickname
		self.values['error'] = error
		self.render('templates/user-login.html')