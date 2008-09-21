#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte at gmail dot com>
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

from google.appengine.ext import db
from google.appengine.api import mail
from handlers.AuthenticatedHandler import *

class GroupForumReply(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		key = self.get_param('key')
		thread = model.Thread.get(key)
		if not thread:
			self.not_found()
			return
		group = thread.group

		response = model.ThreadResponse(thread=thread,
			author=user,
			content=self.get_param('content'))
		response.put()
		
		
		subscribe=self.get_param('subscribe')
		if not user.email in thread.subscribers and subscribe:
			thread.subscribers.append(user.email)
		thread.responses = thread.responses + 1
		thread.put()
		
		self.create_group_subscribers(group)
		group.responses = group.responses + 1
		group.put()
		
		
		subject = u"[debug_mode=ON] Nueva respuesta en: '%s'" % self.clean_ascii(thread.title)

		body = u"""
Nueva respuesta en %s.
Entra en el debate:
http://debugmodeon.com/group.forum/%s

""" % (self.clean_ascii(thread.title), thread.url_path)

		mail.send_mail(sender='contacto@debugmodeon.com',
			to='contacto@debugmodeon.com',
			bcc=thread.subscribers,
			subject=subject,
			body=body)

		self.redirect('/group.forum/%s#comments' % thread.url_path)
