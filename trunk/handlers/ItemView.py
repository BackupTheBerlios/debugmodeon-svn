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
from handlers.BaseHandler import *

class ItemView(BaseHandler):

	def execute(self):
		self.values['tab'] = '/item.list'
		url_path = self.request.path.split('/', 2)[2]
		item = model.Item.gql('WHERE url_path=:1', url_path).get()
		user = self.values['user']
		if not user or item.author.nickname != user.nickname:
			item.views = item.views + 1
			item.put()
		
		if user and user.nickname != item.author.nickname:
			vote = model.Vote.gql('WHERE user=:1 AND item=:2', user, item).get()
			if not vote:
				self.values['canvote'] = True

		self.values['item'] = item
		query = model.Comment.all().filter('item =', item).order('creation_date')
		self.values['comments'] = self.paging(query, 10)
		self.values['keywords'] = ', '.join(item.tags)
		
		groups = [g.group for g in model.GroupItem.all().filter('item =', item)]
		self.values['groups'] = groups
		
		if user and item.author.nickname == user.nickname:
			all_groups = [g.group for g in model.GroupUser.all().filter('user =', user)]
			
			# TODO: this could be improved
			for g in groups:
				for gr in all_groups:
					if str(gr.key()) == str(g.key()):
						all_groups.remove(gr)
				
			self.values['all_groups'] = all_groups
		
		self.render('templates/item-view.html')
