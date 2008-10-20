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
			self.error('Comentario duplicado')
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
			response_number=item.responses+1)
		comment.put()
		
		user.comments += 1
		user.put()

		subscribers = item.subscribers
		if subscribers and user.email in subscribers:
			subscribers.remove(user.email)

		if subscribers:
			app = self.get_application()
			subject = u"Nuevo comentario en: '%s'" % self.clean_ascii(item.title)

			body = u"""
Nuevo comentario en el articulo: '%s':

Lee los comentarios en:
%s/item/%s#comments

""" % (self.clean_ascii(item.title), app.url, item.url_path)
			self.mail(subject=subject, body=body, bcc=item.subscribers)
			
		subscribe = self.get_param('subscribe')
		if subscribe and not user.email in item.subscribers:
			item.subscribers.append(user.email)

		item.responses += 1
		item.put()
		
		page = comment.response_number / 10
		if (comment.response_number % 10) > 0:
			page += 1
		
		self.redirect('/item/%s?p=%d#comment-%d' % (item.url_path, page, comment.response_number))
		
	def check_duplicate(self, item, user, content):
		last_comment = model.Comment.all().filter('item', item).filter('author', user).order('-creation_date').get()
		if last_comment is not None:
			if last_comment.content == content:
				return True
		return False
		
