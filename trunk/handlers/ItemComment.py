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

import time
import datetime

from google.appengine.ext import db
from google.appengine.api import mail
from handlers.AuthenticatedHandler import *

class ItemComment(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		key = self.get_param('key')
		item = model.Item.get(key)
		if not item or item.draft or item.deletion_date:
			self.not_found()
			return
		
		if not self.auth():
			return
		
		content = self.get_param('content')
		preview = self.get_param('preview')
		if preview:
			comment = model.Comment(item=item,
				author=user,
				author_nickname=user.nickname,
				content=content)
			self.values['comment'] = comment
			self.values['preview'] = True
			self.render('templates/item-comment-edit.html')
			return
			
		if self.check_duplicate(item, user, content):
			self.show_error('Comentario duplicado')
			return
		# migration
		if not item.subscribers:
			com = [c.author.email for c in model.Comment.all().filter('item', item).fetch(1000) ]
			com.append(item.author.email)
			item.subscribers = list(set(com))
		# end migration

		comment = model.Comment(item=item,
			author=user,
			author_nickname=user.nickname,
			content=content,
			editions = 0,
			response_number=item.responses+1)
		comment.put()
		results = 10
		app = self.get_application()
		if app.max_results_sublist:
			results = app.max_results_sublist
		page = comment.response_number / results
		if (comment.response_number % results) > 0:
			page += 1
		comment_url = '/item/%s?p=%d#comment-%d' % (item.url_path, page, comment.response_number)
		
		user.comments += 1
		user.put()
		
		item.responses += 1
		item.put()
		
		followers = list(self.get_followers(user=user))
		followers.append(user.nickname)
		followers.extend(self.get_followers(item=item))
		followers = list(set(followers))
		self.create_event(event_type='item.comment',
			followers=followers, user=user, item=item, response_number=comment.response_number)
			
		subscribers = item.subscribers
		if subscribers and user.email in subscribers:
			subscribers.remove(user.email)

		if subscribers:
			subject = u"Nuevo comentario en: '%s'" % self.clean_ascii(item.title)

			body = u"""
Nuevo comentario en el articulo: '%s':
%s%s

Todos los comentarios en:
%s/item/%s#comments

Eliminar suscripcion a este articulo:
%s/item.comment.subscribe?key=%s

""" % (self.clean_ascii(item.title), app.url, comment_url, app.url, item.url_path, app.url, str(item.key()))
			self.mail(subject=subject, body=body, bcc=item.subscribers)
			
		subscribe = self.get_param('subscribe')
		if subscribe and not user.email in item.subscribers:
			item.subscribers.append(user.email)
		
		self.redirect(comment_url)
		
	def check_duplicate(self, item, user, content):
		last_comment = model.Comment.all().filter('item', item).filter('author', user).order('-creation_date').get()
		if last_comment is not None:
			if last_comment.content == content:
				return True
		return False
		
