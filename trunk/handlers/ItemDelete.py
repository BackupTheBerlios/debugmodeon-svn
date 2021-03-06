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

import datetime

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class ItemDelete(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		item = model.Item.get(self.get_param('key'))
		memcache.delete(str(item.key().id()))
		if not item:
			self.not_found()
			return
		
		if user.rol != 'admin' and user.nickname != item.author.nickname:
			self.forbidden()
			return

		if method == 'GET':
			self.values['item'] = item
			self.render('templates/item-delete.html')
		elif self.auth():
			# mark as deleted
			item.deletion_message = self.get_param('message')
			item.deletion_date = datetime.datetime.now()
			item.deletion_user = user
			item.put()
			
			# decrement tag counters
			self.delete_tags(item.tags)
			
			# decrement author counters
			if item.draft:
				item.author.draft_items -= 1
			else:
				item.author.items -=1
			item.author.rating_total -= item.rating_total
			item.author.rating_count -= item.rating_count
			if item.author.rating_count > 0:
				item.author.rating_average = int(item.author.rating_total / item.author.rating_count)
			else:
				item.author.rating_average = 0
			item.author.put()
			
			# decrement group counters and delete relationships
			gi = model.GroupItem.all().filter('item =', item)
			for g in gi:
				g.group.items -= 1
				if g.group.activity:
					g.group.activity -= 15
				g.group
				g.group.put()
				g.delete()
			
			# decrement favourites and delete relationships
			fv = model.Favourite.all().filter('item =', item)
			for f in fv:
				f.user.favourites -= 1
				f.user.put()
				f.delete()
			
			
			rc = model.Recommendation.all().filter('item_from', item)
			for r in rc:
				r.delete()
				
			rc = model.Recommendation.all().filter('item_to', item)
			for r in rc:
				r.delete()
			
			# decrement votes and delete relationships
			# vt = model.Vote.all().filter('item =', item)
			# for v in vt:
			#	v.delete()
			
			# comments?
			memcache.delete('index_items')
			app = model.Application.all().get()
			if app:
				app.items -= 1
				app.put()
			memcache.delete('app')
			
			self.redirect('/item/%s' % item.url_path)
			