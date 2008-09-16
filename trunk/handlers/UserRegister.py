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
from handlers.BaseHandler import *
from google.appengine.ext.webapp import template

class UserRegister(BaseHandler):

	def execute(self):
		method = self.request.method

		if method == 'GET':
			self.values['redirect_to'] = self.request.get('redirect_to')
			self.render('templates/user-register.html')
		else:
			nickname = self.request.get('nickname')
			email = self.request.get('email')
			password = self.request.get('password')
			re_email = self.request.get('re_email')
			re_password = self.request.get('re_password')

			if not self.get_param('terms-and-conditions'):
				self.show_error(nickname, email, u'Debes aceptar los términos y condiciones del servicio')
				return
			
			if not re.match('^[\w\.-]{3,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}$', email):
				self.show_error(nickname, email, 'Introduce una dirección de email válida')
				return

			if not re.match('^[\w\.-]+$', nickname):
				self.show_error(nickname, email, 'El nombre de usuario sólo puede contener letras, números, puntos, guiones y guiones bajos')
				return

			if len(nickname) < 4:
				self.show_error(nickname, email, 'El nombre de usuario debe ser de al menos cuatro caracteres')
				return

			if len(nickname) > 20:
				self.show_error(nickname, email, 'El nombre de usuario no debe ser mayor de 20 caracteres')
				return

			if not password or len(password) < 4 or len(password) > 30:
				self.show_error(nickname, email, 'La contraseña debe ser de entre cuatro y doce caracteres')
				return

			u = model.UserData.all().filter('nickname =', nickname).get()
			if u:
				self.show_error(nickname, email, 'El nombre de usuario ya existe')
				return
			
			u = model.UserData.all().filter('email =', email).get()
			if u:
				self.show_error(nickname, email, 'Ya existe una cuenta con esa dirección de correo electrónico')
				return
				
			if email != re_email:
				self.show_error(nickname, email, 'El e-mail y el e-mail repetido no son iguales')
				return
				
			if password != re_password:
				self.show_error(nickname, email, 'La contraseña y la contraseña repetida no son iguales')
				return
			
			user = model.UserData(nickname=nickname,
				email=email,
				password=self.hash(nickname, password),
				items=0,
				draft_items=0,
				messages=0,
				draft_messages=0,
				comments=0,
				rating_count=0,
				rating_total=0,
				rating_average=0,
				threads=0,
				responses=0,
				groups=0,
				favourites=0,
				public=False)
			user.put()

			self.sess = session.Session()
			self.sess['user_nickname'] = user.nickname
			self.sess['user_email'] = user.email
			self.sess['user_key'] = user.key()
			self.sess['user'] = user
			rt = self.request.get('redirect_to')
			if not rt:
				rt = '/'
			self.redirect(rt)

	def show_error(self, nickname, email, error):
		self.values['nickname'] = nickname
		self.values['email'] = email
		self.values['error'] = error
		self.render('templates/user-register.html')
	
	def match(self, pattern, value):
		m = re.match(pattern, value)
		if not m or not m.string[m.start():m.end()] == value:
			return None
		return value