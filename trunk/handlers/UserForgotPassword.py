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

from handlers.BaseHandler import *
from google.appengine.api import mail

class UserForgotPassword(BaseHandler):

	def execute(self):
		method = self.request.method
		
		if method == 'GET':
			self.values['redirect_to'] = self.request.get('redirect_to')
			self.render('templates/user-forgotpassword.html')
		else:
			email = self.request.get('email')
			u = model.UserData.all().filter('email =', email).get()
			if not u:
				self.show_error(email, 'No se encuentra un usuario con esa dirección')
				return
			
			u.token = self.hash(str(random.random()), email)
			u.put()
			
			# TODO send mail
			subject = "[debug_mode=ON] Recuperar password"
			
			body = """
Haz click en el siguiente enlace para proceder a establecer tu password
http://debugmodeon.com/user.resetpassword?nickname=%s&token=%s
   
""" % (u.nickname, u.token)
   
			mail.send_mail('contacto@debugmodeon.com', u.email, subject, body)
			
			self.values['token'] = u.token
			self.values['email'] = email
			self.values['redirect_to'] = self.request.get('redirect_to')
			self.render('templates/user-forgotpassword-sent.html')

	def show_error(self, email, error):
		self.values['email'] = email
		self.values['error'] = error
		self.render('templates/user-forgotpassword.html')