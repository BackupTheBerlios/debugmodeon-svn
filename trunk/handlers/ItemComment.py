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
		
		if item.draft:
			self.redirect('/item/%s#comments' % (item.url_path, ))
			return
		comment = model.Comment(item=item, author=user, content=self.get_param('content'))
		comment.put()
		item.responses = item.responses + 1
		item.put()
		
		user.comments += 1
		user.put()
		
		subject = u"[debug_mode=ON] Comentario: '%s'" % item.url_path

		body = u"""
Nuevo comentario en el siguiente articulo:
http://debugmodeon.com/item/%s#comments

""" % item.url_path
		
		mail.send_mail(user.email, item.author.email, subject, body)
		
		self.redirect('/item/%s#comments' % (item.url_path, ))