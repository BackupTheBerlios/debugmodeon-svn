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

import logging
import datetime

from google.appengine.runtime import apiproxy_errors
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import memcache
from handlers.AuthenticatedHandler import *

class GroupForumEdit(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		if method == "GET":
			return
		user = self.values['user']
		key = self.get_param('key')
		group = model.Group.get(key)
		if not group:
			self.not_found()
			return
		
		if group.all_users is not None and not self.can_write(group):
			self.forbidden()
			return
		title = self.get_param('title')
		url_path = ''
		content = self.get_param('content')
		preview = self.get_param('preview')
		if preview:
			thread = model.Thread(group=group,
				group_url_path=group.url_path,
				author=user,
				author_nickname = user.nickname,
				title=title,
				content=content,
				responses=0)
			self.values['thread'] = thread
			self.values['preview'] = True
			self.values['is_parent_thread'] = True
			self.render('templates/group-thread-edit.html')
			return
		
		if self.check_duplicate(group, user, content, title):
			self.error('Hilo duplicado')
			return
		thread = model.Thread(group=group,
			group_title=group.title,
			group_url_path=group.url_path,
			author=user,
			author_nickname=user.nickname,
			title=title,
			url_path=url_path,
			content=content,
			last_response_date = datetime.datetime.now(),
			responses=0,
			editions=0,
			views=0)
		
		user.threads += 1
		user.put()
		
		self.create_group_subscribers(group)
		
		app = model.Application.all().get()
		if app:
			if not app.threads:
				app.threads = 0
			app.threads += 1
			app.put()
		memcache.delete('app')
		
		thread.put()
		thread.url_path = ('%d/%s/%s') % (thread.key().id(), self.to_url_path(group.title), self.to_url_path(title))
		subscribe = self.get_param('subscribe')
		if subscribe:
			thread.subscribers.append(user.email)
			self.add_user_subscription(user, 'thread', thread.key().id())
		thread.put()
		group.threads += 1
		if group.activity:
			group.activity += 5
		group.put()
		
		subscribers = group.subscribers
		if subscribers and user.email in subscribers:
			subscribers.remove(user.email)

		if subscribers:
			app = self.get_application()
			subject = "Nueva tema: '%s'" % self.clean_ascii(thread.title)

			body = u"""
Nuevo tema en el grupo %s.
Titulo del tema: %s
Entra en el debate:
%s/group.forum/%s

""" % (self.clean_ascii(group.title), self.clean_ascii(thread.title), app.url, thread.url_path)
			self.mail(subject=subject, body=body, bcc=group.subscribers)
		
			
		
		memcache.delete('index_threads')

		self.redirect('/group.forum/%s' % thread.url_path)

	def check_duplicate(self, group, user, content, title):
		last_thread = model.Thread.all().filter('group', group).filter('parent_thread', None).filter('author', user).order('-creation_date').get()
		if last_thread is not None:
			if last_thread.title == title and last_thread.content == content:
				return True
		return False
		