#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte@gmail.com>,
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
from handlers.AuthenticatedHandler import *

class ItemFavourite(AuthenticatedHandler):
	
	def execute(self):
		item = model.Item.get(self.get_param('key'))
		user = self.values['user']
		if not item or item.draft or item.deletion_date:
			self.not_found()
			return
		
		if not self.auth():
			return

		favourite = model.Favourite.gql('WHERE user=:1 AND item=:2', user, item).get()
		if not favourite:
			favourite = model.Favourite(item=item,
				user=user,
				item_author_nickname=item.author_nickname,
				item_title=item.title,
				item_url_path=item.url_path,
				user_nickname=user.nickname)
			favourite.put()

			user.favourites += 1
			user.put()
			
			followers = list(self.get_followers(user=user))
			followers.append(user.nickname)
			followers.extend(self.get_followers(item=item))
			followers = list(set(followers))
			self.create_event(event_type='item.favourite', followers=followers, user=user, item=item)
			
			if self.get_param('x'):
				self.render_json({ 'action': 'added' })
			else:
				self.redirect('/item/%s' % item.url_path)
		else:
			favourite.delete()
			
			user.favourites -= 1
			user.put()
		
			if self.get_param('x'):
				self.render_json({ 'action': 'deleted' })
			else:
				self.redirect('/item/%s' % item.url_path)
