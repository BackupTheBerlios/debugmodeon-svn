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

from google.appengine.ext import db
from handlers.BaseHandler import *

class ItemView(BaseHandler):

	def execute(self):
		url_path = self.request.path.split('/', 2)[2]
		item = model.Item.get_by_id(int(self.request.path.split('/')[2]))
		
		if not item:
			self.not_found()
			return
		
		if item.url_path != url_path:
			self.redirect('/item/%s' % item.url_path, permanent=True)
			return
		
		self.values['tab'] = '/item.list'
		user = self.values['user']
		if item.draft:
			if not user or not user.nickname == item.author.nickname:
				self.forbidden()
				return
		
		if not user or item.author.nickname != user.nickname:
			item.views = item.views + 1
			item.put()
		
		if user and user.nickname != item.author.nickname:
			vote = model.Vote.gql('WHERE user=:1 AND item=:2', user, item).get()
			if not vote:
				self.values['canvote'] = True
		if user:
			added = model.Favourite.gql('WHERE user=:1 AND item=:2',user,item).get()
			if not added:
				self.values['canadd'] = True
		
		
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
		
		related = model.Item.all() \
			.filter('author =', item.author) \
			.filter('draft =', False) \
			.order('-rating_average').fetch(11)
		related = [i for i in related]
		if item in related:
			related.remove(item)
		else:
			related = related[:-1]
		
		self.values['related'] = related
		self.render('templates/item-view.html')
