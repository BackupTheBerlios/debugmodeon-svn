#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
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

import re
import random
import model

from handlers.BaseHandler import *

from os import environ
from recaptcha import captcha

class UserRegister(BaseHandler):

	def execute(self):
		method = self.request.method
		if method == 'GET':
			self.send_form(None)
		else:
			if self.get_param('x'):
				# check if nickname is available
				nickname = self.request.get('nickname')
				email = self.request.get('email')
				message = self.validate_nickname(nickname)
				if message:
					self.render_json({'valid': False, 'message': message})
				else :
					self.render_json({'valid': True })
				return
			else:
				# Validate captcha
				challenge = self.request.get('recaptcha_challenge_field')
				response  = self.request.get('recaptcha_response_field')
				remoteip  = environ['REMOTE_ADDR']

				cResponse = captcha.submit(
					challenge,
					response,
					self.get_application().recaptcha_private_key,
					remoteip)

				if not cResponse.is_valid:
					# If the reCAPTCHA server can not be reached, 
					# the error code recaptcha-not-reachable will be returned.
					self.send_form(cResponse.error_code)
					return
				
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
					self.show_error(nickname, email, u'El nombre de usuario sólo puede contener letras, números, puntos, guiones y guiones bajos')
					return

				if not password or len(password) < 4 or len(password) > 30:
					self.show_error(nickname, email, u'La contraseña debe ser de entre cuatro y treinta caracteres')
					return
				message = self.validate_nickname(nickname)
				if message:
					self.show_error(nickname, email, message)
					return
			
				u = model.UserData.all().filter('email =', email).get()
				if u:
					self.show_error(nickname, email, u'Ya existe una cuenta con esa dirección de correo electrónico')
					return
				
				if email != re_email:
					self.show_error(nickname, email, 'El e-mail y el e-mail repetido no son iguales')
					return
				
				if password != re_password:
					self.show_error(nickname, email, u'La contraseña y la contraseña repetida no son iguales')
					return
			
					times = 5
			
				user = model.UserData(nickname=nickname,
					email=email,
					password=self.hash_password(nickname, password),
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
					public=False,
					contacts=0)
				user.put()
				
				app = model.Application.all().get()
				if app:
					app.users += 1
					app.put()
				memcache.delete('app')

				#send welcome email
				app = self.get_application()
				subject = "Bienvenido a debug_mode=ON"
				body = u"""
Gracias por registrarte en debug_mode=ON. El equipo de debug_mode=ON te damos la bienvenida.

Completa tu perfil con tu información 
%s/user.edit

Publica artículos, ¡puedes ganar dinero!. 
Informaté en http://www.debugmodeon.com/item/5674/como-anadir-adsense-a-tus-articulos

Forma parte de los grupos que te interesan. Cada grupo tiene un foro, para compartir o debatir con las personas a las que les interese lo mismo que a ti.
Listado de grupos %s/group.list
Listado de hilos %s/forum.list

Sugerencias, opiniones, nos gustaría tener tu feedback 
http://www.debugmodeon.com/group.forum/9240/debug-mode-on/opiniones-sugerencias-feedback-general

Para más información tenemos una sección de FAQ
%s/html/faq.html

Atentamente,

El equipo de debug_mode=ON.

""" % (app.url, app.url, app.url, app.url)
				self.mail(subject=subject, body=body, to=[user.email])
				self.sess.store(str(user.key()), 7200)
				rt = self.request.get('redirect_to')
				if not rt:
					rt = '/'
				self.redirect(rt)

	def show_error(self, nickname, email, error):
		chtml = self.get_captcha(None)
		self.values['captchahtml'] = chtml
		self.values['nickname'] = nickname
		self.values['email'] = email
		self.values['error'] = error
		self.render('templates/user-register.html')
	
	def match(self, pattern, value):
		m = re.match(pattern, value)
		if not m or not m.string[m.start():m.end()] == value:
			return None
		return value
		
	def send_form(self, error):
		chtml = self.get_captcha(error)
		self.values['captchahtml'] = chtml
		self.values['redirect_to'] = self.request.get('redirect_to')
		self.render('templates/user-register.html')
		
	def get_captcha(self, error):
		chtml = captcha.displayhtml(
			public_key = self.get_application().recaptcha_public_key,
			use_ssl = False,
			error = error)
		return chtml

	def validate_nickname(self, nickname):
		if len(nickname) < 4:
			return 'El nombre de usuario debe ser de al menos cuatro caracteres'

		if len(nickname) > 20:
			return 'El nombre de usuario no debe ser mayor de 20 caracteres'

		u = model.UserData.all().filter('nickname =', nickname).get()
		if u:
			return 'El nombre de usuario ya existe'
			
		return ''