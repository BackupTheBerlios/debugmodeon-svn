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

from handlers.AuthenticatedHandler import *

class AdminCategoryEdit(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		self.values['tab'] = '/admin'

		if user.rol != 'admin':
			self.forbidden()
			return
			
		key = self.get_param('key')
		self.values['parent_categories'] = list(model.Category.all().filter('parent_category', None).order('title'))
		self.values['parent_category'] = None

		if method == 'GET':
			if key:
				# show edit form
				category = model.Category.get(key)
				self.values['key'] = key

				self.values['title'] = category.title
				self.values['description'] = category.description
				self.values['parent_category'] = category.parent_category
				self.render('templates/admin-category-edit.html')
			else:
				# show an empty form
				self.values['key'] = None
				self.values['title'] = u'Nueva categoría...'
				self.values['description'] = u'Descripción...'
				self.render('templates/admin-category-edit.html')
		elif self.auth():
			if key:
				# update category
				category = model.Category.get(key)
				category.title = self.get_param('title')
				category.description = self.get_param('description')
				category.url_path = self.to_url_path(category.title)
				parent_key = self.request.get('parent_category')
				if parent_key:
					category.parent_category = model.Category.get(parent_key)
				category.put()
				self.redirect('/admin.categories')
			else:
				category = model.Category(title=self.get_param('title'),
					description=self.get_param('description'),
					items = 0,
					groups = 0)
				category.url_path = self.to_url_path(category.title)
				parent_key = self.request.get('parent_category')
				if parent_key:
					category.parent_category = model.Category.get(parent_key)
				category.put()
				self.redirect('/admin.categories')