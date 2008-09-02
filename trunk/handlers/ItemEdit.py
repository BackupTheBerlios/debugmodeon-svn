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

import time
import datetime

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class ItemEdit(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')
		
		licenses = [ { 'id': 'copyright', 'lic': '&copy; Todos los derechos reservados' },
			{ 'id': 'pd', 'lic': 'Dominio público' },
			{ 'id': 'by', 'lic': 'Creative Commons: Reconocimiento' },
			{ 'id': 'by-nc', 'lic': 'Creative Commons: Reconocimiento-No comercial' },
			{ 'id': 'by-nc-nd', 'lic': 'Creative Commons: Reconocimiento-No comercial-Sin obras derivadas' },
			{ 'id': 'by-nc-sa', 'lic': 'Creative Commons: Reconocimiento-No comercial-Compartir bajo la misma licencia' },
			{ 'id': 'by-nd', 'lic': 'Creative Commons: Reconocimiento-Sin obras derivadas' },
			{ 'id': 'by-sa', 'lic': 'Creative Commons: Reconocimiento-Compartir bajo la misma licencia' }
		]
		self.values['licenses'] = licenses
		
		if method == 'GET':
			if key:
				# show edit form
				item = model.Item.get(key)
				if not user.nickname == item.author.nickname:
					self.forbidden()
					return
				self.values['key'] = key
				
				self.values['title'] = item.title
				self.values['lic'] = item.lic
				self.values['tags'] = ', '.join(item.tags)
				self.values['description'] = item.description
				self.values['content'] = item.content
				self.render('templates/item-edit.html')
			else:
				# show an empty form
				self.values['title'] = 'Título...'
				self.values['lic'] = 'copyright'
				self.render('templates/item-edit.html')
		else:
			if key:
				# update item
				item = model.Item.get(key)
				if not user.nickname == item.author.nickname:
					self.forbidden()
					return
				self.delete_tags(item.tags)
				item.title = self.get_param('title')
				item.lic = self.get_param('lic')
				item.tags = [self.to_url_path(t) for t in self.get_param('tags').split(',')]
				item.description = ' '.join(self.get_param('description').splitlines())
				item.content = self.get_param('content')
				item.put()
				self.update_tags(item.tags)
				self.redirect('/item/%s' % (item.url_path, ))
			else:
				# new item
				today = datetime.date.today()
				title = self.get_param('title')
				url_path = '%02d/%02d/%d/%s' % (today.day, today.month, today.year, self.to_url_path(title))
				url_path = self.unique_url_path(model.Item, url_path)
				tags = [self.to_url_path(t) for t in self.get_param('tags').split(',')]
				
				item = model.Item(author=user,
					title=title,
					description=' '.join(self.get_param('description').splitlines()),
					content=self.get_param('content'),
					lic=self.get_param('lic'),
					url_path=url_path,
					tags=tags,
					draft=False,
					item_type='article',
					views=0,
					responses=0,
					rating_count=0,
					rating_total=0)
				item.put()
				
				user.items += 1
				user.put()
				
				self.update_tags(tags)

				self.redirect('/item/%s' % (item.url_path, ))