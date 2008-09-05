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
			
			email = self.match('[\w\.-]{3,}@([\w-]{2,}\.)*([\w-]{2,}\.)[\w-]{2,4}', email)
			
			if not email:
				self.error(nickname, self.request.get('email'), 'Introduce una dirección de email válida')
				return

			nickname = self.match('[a-zA-Z0-9\.-]*', nickname)

			if not nickname:
				self.error(self.request.get('nickname'), email, 'El nombre de usuario sólo puede contener letras, números, guiones o puntos')
				return

			if len(nickname) < 4:
				self.error(nickname, email, 'El nombre de usuario debe ser de al menos cuatro caracteres')
				return
			
			if not password or len(password) < 4:
				self.error(nickname, email, 'La contraseña debe ser de al menos cuatro caracteres')
				return

			u = model.UserData.all().filter('nickname =', nickname).get()
			if u:
				self.error(nickname, email, 'El nombre de usuario ya existe')
				return
			
			u = model.UserData.all().filter('email =', email).get()
			if u:
				self.error(nickname, email, 'Ya existe una cuenta con esa dirección de correo electrónico')
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

	def error(self, nickname, email, error):
		self.values['nickname'] = nickname
		self.values['email'] = email
		self.values['error'] = error
		self.render('templates/user-register.html')
	
	def match(self, pattern, value):
		m = re.match(pattern, value)
		if not m or not m.string[m.start():m.end()] == value:
			return None
		return value