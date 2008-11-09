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

import datetime

from google.appengine.runtime import apiproxy_errors
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import memcache
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
		if group.all_users is not None and not self.can_write(group):
			self.forbidden()
			return
		content = self.get_param('content')
		if self.check_duplicate(group, user, thread, content):
			self.error('Respuesta duplicada')
			return
		response = model.Thread(group=group,
			group_title=group.title,
			group_url_path=group.url_path,
			author=user,
			author_nickname=user.nickname,
			title=thread.title,
			url_path=thread.url_path,
			content=content,
			parent_thread=thread,
			response_number=thread.responses+1,
			responses=0,
			editios=0)
		response.put()

		page = response.response_number / 20
		if (response.response_number % 20) > 0:
			page += 1
		response_url = '/group.forum/%s?p=%d#comment-%d' % (thread.url_path, page, response.response_number)
					
		self.create_group_subscribers(group)
		group.responses = group.responses + 1
		group.put()
		
		subscribers = thread.subscribers
		if subscribers and user.email in subscribers:
			subscribers.remove(user.email)

		if subscribers:
			app = self.get_application()
			subject = "Nueva respuesta en: '%s'" % self.clean_ascii(thread.title)

			body = u"""
Nueva respuesta en %s.
%s%s

Todas las respuestas:
%s/group.forum/%s

Eliminar suscripcion a este hilo:
%s/group.forum.subscribe?key=%s

""" % (self.clean_ascii(thread.title), app.url, response_url, app.url, thread.url_path, app.url, str(thread.key()))
			self.mail(subject=subject, body=body, bcc=thread.subscribers)
		
		subscribe = self.get_param('subscribe')
		if subscribe and not user.email in thread.subscribers:
			thread.subscribers.append(user.email)
			self.add_user_subscription(user, 'thread', thread.key().id())
		thread.responses += 1
		thread.last_response_date = datetime.datetime.now()
		thread.put()
		
		group = thread.group
		if group.activity:
			group.activity += 2
		group.put()
		memcache.delete('index_threads')

		self.redirect(response_url)
		
	def check_duplicate(self, group, user, parent_thread, content):
		last_thread = model.Thread.all().filter('group', group).filter('parent_thread', parent_thread).filter('author', user).order('-creation_date').get()
		if last_thread is not None:
			if last_thread.content == content:
				return True
		return False
