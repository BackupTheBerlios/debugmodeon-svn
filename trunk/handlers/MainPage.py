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

from google.appengine.api import memcache
from handlers.BaseHandler import *

class MainPage(BaseHandler):

	def execute(self):
		self.values['tab'] = '/'
		self.values['items'] = self.cache('index_items', self.get_items)
		self.values['groups'] = self.cache('index_groups', self.get_groups)
		# self.values['users'] = model.UserData.all().filter('items >', 0).order('-items').fetch(5)
		self.values['threads'] = self.cache('index_threads', self.get_threads)
		
		self.values['taglist'] = self.cache('taglist', self.get_taglist)
		self.render('templates/index.html')
	
	def get_taglist(self):
		return self.tag_list(model.Tag.all())
		
	def get_items(self):
		return model.Item.all().filter('draft', False).filter('deletion_date', None).order('-creation_date').fetch(10)

	def get_groups(self):
		return model.Group.all().order('-creation_date').fetch(10)

	def get_threads(self):
		return model.Thread.all().order('-last_update').fetch(10)
		
	def cache(self, key, function, timeout=600):
		data = memcache.get(key)
		if data is not None:
			return data
		else:
			data = function.__call__()
			memcache.add(key, data, 600)
			return data
