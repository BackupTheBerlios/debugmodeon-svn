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

from handlers.AuthenticatedHandler import *

class MessageEdit(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		user_to = model.UserData.all().filter('nickname', self.get_param('user_to')).get()
		if not user_to:
			self.not_found()
			return
			
		method = self.request.method
		if method == 'GET':
			self.values['user_to'] = self.get_param('user_to')
			title = self.get_param('title')
			if not title:
				title = 'Nuevo mensaje...'
			elif not title.startswith('Re:'):
				title = 'Re:%s' % title
			self.values['title'] = title
			self.render('templates/message-edit.html')
			return
		elif self.auth():
			title = self.get_param('title')
			message = model.Message(user_from = user,
				user_from_nickname = user.nickname,
				user_to = user_to,
				user_to_nickname = user_to.nickname,
				content=self.get_param('content'),
				title=self.get_param('title'),
				url_path = '-',
				read=False)
			message.put()
			message.url_path = ('%d/%s') % (message.key().id(), self.to_url_path(title))
			message.put()
			
			if not user.sent_messages:
				user.sent_messages = 0
			if not user_to.unread_messages:
				user_to.unread_messages = 0
				
			user.sent_messages += 1
			user_to.unread_messages += 1
			
			user.put()
			user_to.put()
			
			app = self.get_application()
			subject = "%s te ha enviado un mensaje" % user.nickname

			body = u"""
%s te ha enviado un mensaje.
Leelo en:
%s/message.inbox

""" % (user.nickname, app.url)
			self.mail(subject=subject, body=body, to=[user_to.email])

			self.redirect('/message.sent')

