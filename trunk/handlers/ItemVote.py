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
from handlers.AuthenticatedHandler import *

class ItemVote(AuthenticatedHandler):
	
	def execute(self):
		item = model.Item.get(self.get_param('key'))
		if not item or item.draft or item.deletion_date:
			self.not_found()
			return
		
		if not self.auth():
			return
		memcache.delete(str(item.key().id()) + '_item')
		rating = int(self.get_param('rating'))
		if rating < 0:
			rating = 0
		elif rating > 5:
			rating = 5
		
		user = self.values['user']
		avg = item.rating_average
		
		if item and item.author.nickname != user.nickname:
			vote = model.Vote.gql('WHERE user=:1 and item=:2', user, item).get()
			if not vote:
				vote = model.Vote(user=user,rating=rating,item=item)
				vote.put()
   
				item.rating_count += 1
				item.rating_total += rating
				item.rating_average = int(item.rating_total / item.rating_count)
				item.put()
   
				author = item.author
				author.rating_count += 1
				author.rating_total += rating
				author.rating_average = int(author.rating_total / author.rating_count)
				author.put()
				avg = item.rating_average
		memcache.add(str(item.key().id()) + '_item', item, 0)
		
		if self.get_param('x'):
			self.render_json({ 'average': avg, 'votes': item.rating_count })
		else:
			self.redirect('/item/%s' % item.url_path)
