#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Juan Luis Belmonte  <jlbelmonte at gmail dot com> 
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
from handlers.AuthenticatedHandler import *


class ItemCommentSubscribe( AuthenticatedHandler ):

	def execute(self):
		key  = self.get_param('key')
		item = model.Item.get(key)
		user = self.values['user']
		mail = user.email
		
		if not mail in item.subscribers:
			if not self.auth():
				return
			item.subscribers.append(mail)
			item.put()
			self.add_user_subscription(user, 'item', item.key().id())
			if self.get_param('x'):
				self.render_json({ 'action': 'subscribed' })
			else:
				self.redirect('/item/%s' % (item.url_path, ))
		else:
			auth = self.get_param('auth')
			if not auth:
				self.values['item'] = item
				self.render('templates/item-comment-subscribe.html')
			else:
				if not self.auth():
					return
				item.subscribers.remove(mail)
				item.put()
				self.remove_user_subscription(user, 'item', item.key().id())
				if self.get_param('x'):
					self.render_json({ 'action': 'unsubscribed' })
				else:
					self.redirect('/item/%s' % (item.url_path, ))

