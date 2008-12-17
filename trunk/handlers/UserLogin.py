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
import random
import datetime

from handlers.BaseHandler import *

class UserLogin(BaseHandler):
	
	def execute(self):
		self.sess.valid = False
		
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
					if user.banned_date is not None:
						self.show_error(nickname, u'Usuario baneado. Póngase en contacto con un administrador.')
						return
					user.last_login = datetime.datetime.now()
					user.password = self.hash_password(user.nickname, password) # if you want to change the way the password is hashed
					user.put()
					if self.get_param('remember') == 'remember':
						expires = 1209600
					else:
						expires = 7200
					self.sess.store(str(user.key()), expires)
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