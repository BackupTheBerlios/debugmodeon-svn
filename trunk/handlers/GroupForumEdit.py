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

from google.appengine.ext import db
from google.appengine.api import mail
from handlers.AuthenticatedHandler import *

class GroupForumEdit(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		key = self.get_param('key')
		group = model.Group.get(key)
		if not group:
			self.not_found()
			return
		
		title = self.get_param('title')
		url_path = ('%s/%s') % (group.url_path, self.to_url_path(title))
		url_path = self.unique_url_path(model.Thread, url_path)

		thread = model.Thread(group=group,
			author=user,
			title=title,
			url_path=url_path,
			content=self.get_param('content'),
			responses=0,
			subscribers=[ user.email ])
		thread.put()
		
		user.threads += 1
		user.put()
		
		self.create_group_subscribers(group)
		subscribe=self.get_param('subscribe')
		if not user.email in thread.subscribers and subscribe:
			thread.subscribers.append(user.email)

		group.threads += 1
		group.put()
		
		subject = u"[debug_mode=ON] Nuevo tema: '%s'" % self.clean_ascii(thread.title)

		body = u"""
Nuevo tema en el grupo %s.
Titulo del tema: %s
Entra en el debate:
http://debugmodeon.com/group.forum/%s

""" % (self.clean_ascii(group.title), self.clean_ascii(thread.title), thread.url_path)

		mail.send_mail(sender='contacto@debugmodeon.com',
			to='contacto@debugmodeon.com',
			bcc=group.subscribers,
			subject=subject,
			body=body)

		self.redirect('/group.forum/%s' % thread.url_path)
