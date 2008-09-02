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
		rating = int(self.get_param('rating'))
		if rating < 0:
			rating = 0
		else if rating > 5:
			rating = 5
		
		if item:
			vote = model.Vote(user=self.values['user'],rating=rating,item=item)
			vote.put()

			item.rating_count = += 1
			item.rating_total = += vote.rating
			item.rating_average = int(item.rating_total / item.rating_count)
			item.put()

			user = model.UserData.gql('WHERE nickname=:1', item.author.nickname()).get()
			user.rating_count = += 1
			user.rating_total = += vote.rating
			user.rating_average = int(user.rating_total / user.rating_count)
			user.put()
				
		self.redirect('/item/%s' % item.url_path)
