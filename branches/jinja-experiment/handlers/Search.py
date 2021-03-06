#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# (C) Copyright 2008 Ignacio Andreu <plunchete at gmail dot com>
# (C) Copyright 2008 Néstor Salceda <nestor.salceda at gmail dot com>
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

class Search(BaseHandler):

	def execute(self):
		q = self.get_param('q')
		item_type = self.get_param('item_type')

		if item_type == 'items':
			query = model.Item.all().filter('draft =', False).filter('deletion_date', None).search(q)
			self.values['items'] = self.paging(query, 10)
		# elif item_type == 'users':
		#	query = model.UserData.all().search(q)
		#	self.values['users'] = self.paging(query, 10)
		# elif item_type == 'groups':
		else:
			query = model.Group.all().search(q)
			self.values['groups'] = self.paging(query, 10)

		self.values['taglist'] = self.tag_list(model.Tag.all())
		self.values['q'] = q
		self.values['item_type'] = item_type
		self.render('templates/search.html')
