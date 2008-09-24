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

from google.appengine.api import mail
from handlers.AuthenticatedHandler import *

class UserContact(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		user_to = model.UserData.all().filter('nickname', self.get_param('user_to')).get()
		if not user_to:
			self.not_found()
			return
		
		contact = model.Contact.all().filter('user_from', user).filter('user_to', user_to).get()
		if not contact:
			contact = model.Contact(user_from=user, user_to=user_to)
			contact.put()
			
			user.contacts += 1
			user.put()
			
			subject = "[debug_mode=ON] %s te ha agregado como contacto" % user.nickname

			body = """
%s te ha agregado como contacto en http://debugmodeon.com
Puedes visitar su perfil en: http://debugmodeon.com/user/%s

""" % (user.nickname, user.nickname)

			mail.send_mail('contacto@debugmodeon.com', user_to.email, subject, body)
			
			if self.get_param('x'):
				self.render_json({ 'action': 'added' })
			else:
				self.redirect('/user/%s' % user_to.nickname)
		else:
			contact.delete()
			
			user.contacts -= 1
			user.put()
			
			if self.get_param('x'):
				self.render_json({ 'action': 'deleted' })
			else:
				self.redirect('/user/%s' % user_to.nickname)
