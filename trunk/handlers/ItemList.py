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
		query = model.Item.all().filter('draft =', False).filter('deletion_date', None)
		app = self.get_application()
		key = '%s?%s' % (self.request.path, self.request.query)
		results = 10
		if app.max_results:
			results = app.max_results
		self.values['items'] = self.paging(query, results, '-creation_date', app.items, ['-creation_date', '-rating_average', '-responses'], key)
		self.add_tag_cloud()
		self.render('templates/item-list.html')
