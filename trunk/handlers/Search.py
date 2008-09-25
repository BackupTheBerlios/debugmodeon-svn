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

	def is_added (self, thread, threads):
		for current in threads:
			if thread.key() == current.key():
				return True
		return False

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
		elif item_type == 'forums':
			query = model.Thread.all ().search(q)
			values = []
			#Pre pagination
			try:
				counter = int (self.get_param ("p")) * 10
			except ValueError:
				counter = 0
			current = query.fetch (1, counter)
			#We do the post paging here
			while len (values) != 10 and len(current) == 1 :
				counter = counter + 1
				#Use only the top level threads for showing
				while current[0].parent_thread is not None:
					current[0] = current[0].parent_thread
				#Avoid repeating results
				if not self.is_added (current[0], values):
					values.append (current[0])

				current = query.fetch (1, counter)
			self.values['threads'] = values 
		else:
			query = model.Group.all().search(q)
			self.values['groups'] = self.paging(query, 10)

		self.values['taglist'] = self.tag_list(model.Tag.all())
		self.values['q'] = q
		self.values['item_type'] = item_type
		self.render('templates/search.html')
