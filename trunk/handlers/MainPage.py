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

class MainPage(BaseHandler):

	def execute(self):
		self.values['tab'] = '/'
		# memcache.delete('index_items')
		# memcache.delete('index_groups')
		# memcache.delete('index_threads')
		self.values['items'] = self.cache('index_items', self.get_items)
		self.values['groups'] = self.cache('index_groups', self.get_groups)
		self.values['threads'] = self.cache('index_threads', self.get_threads)
		self.add_tag_cloud()
		self.render('templates/index.html')
		
	def get_items(self):
		items = model.Item.all().filter('draft', False).filter('deletion_date', None).order('-creation_date').fetch(10)
		return self.render_chunk('templates/index-items.html', {'items': items})

	def get_groups(self):
		groups = model.Group.all().order('-members').fetch(10)
		return self.render_chunk('templates/index-groups.html', {'groups': groups})

	def get_threads(self):
		threads = model.Thread.all().filter('parent_thread', None).order('-last_response_date').fetch(10)
		return self.render_chunk('templates/index-threads.html', {'threads': threads})
