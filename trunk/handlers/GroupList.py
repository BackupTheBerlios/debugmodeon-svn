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

from handlers.BaseHandler import *

class GroupList(BaseHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		query = model.Group.all()
		key = '%s?%s' % (self.request.path, self.request.query)
		
		cat = self.get_param('cat')
		if cat:
			category = model.Category.all().filter('url_path', cat).get()
			self.values['category'] = category
			self.values['cat'] = cat
			query = query.filter('category', category)
			max = category.groups
		else:
			app = self.get_application()
			max = app.groups
			
		groups = self.paging(query, 10, '-members', max, ['-creation_date', '-members', '-items'], key)
		self.values['groups'] = groups
		# denormalization
		for g in groups:
			if not g.owner_nickname:
				g.owner_nickname = g.owner.nickname
				g.put()
		self.add_categories()
		self.render('templates/group-list.html')
