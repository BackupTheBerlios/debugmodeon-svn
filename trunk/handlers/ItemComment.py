#!/usr/bin/python
# -*- coding: utf-8 -*-

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
		
		comment = model.Comment(item=item, author=user, content=self.get_param('content'))
		comment.put()
		item.responses = item.responses + 1
		item.put()
		
		user_data = model.UserData.gql('WHERE email=:1', user.email()).get()
		user_data.comments = user_data.comments + 1
		user_data.put()
		
		subject = u"[debug_mode=ON] Comentario: '%s'" % item.url_path

		body = u"""
Nuevo comentario en el siguiente articulo:
http://debugmodeon.com/item/%s#comments

""" % item.url_path
		
		mail.send_mail(user.email(), item.author.email(), subject, body)
		
		self.redirect('/item/%s#comments' % (item.url_path, ))