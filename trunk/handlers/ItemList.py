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

from handlers.BaseHandler import *

class ItemList(BaseHandler):

	def execute(self):
		self.values['tab'] = '/item.list'
		self.values['items'] = self.post_pag(self.get_items(), 10) #self.post_pag(self.cache_this(self.get_items), 10)
		self.values['taglist'] = [] # self.tag_list(model.Tag.all())
		self.render('templates/item-list.html')
	
	def get_items(self):
		query = model.Item.all().filter('draft =', False).filter('deletion_date', None).order('-creation_date')
		items = self.pre_pag(query, 10)
		for i in items:
			if not i.author_nickname:
				i.author_nickname = i.author.nickname
				i.put()
		return items
