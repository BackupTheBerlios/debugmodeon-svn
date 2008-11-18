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

import time
import datetime

from google.appengine.ext import db
from google.appengine.api import memcache
from handlers.AuthenticatedHandler import *

class ItemEdit(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')
		x = self.get_param('x')
		draft = False
		if self.get_param('save_draft'):
			draft = True
		
		licenses = [ { 'id': 'copyright', 'lic': '&copy; Todos los derechos reservados' },
			{ 'id': 'pd', 'lic': u'Dominio público' },
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
				if not item:
					self.not_found()
					return
				if not user.nickname == item.author.nickname and user.rol != 'admin':
					self.forbidden()
					return
				self.values['key'] = key
				
				self.values['title'] = item.title
				self.values['lic'] = item.lic
				self.values['tags'] = ', '.join(item.tags)
				self.values['description'] = item.description
				self.values['content'] = item.content
				self.values['draft'] = item.draft
				self.render('templates/item-edit.html')
			else:
				# show an empty form
				self.values['title'] = u'Título...'
				self.values['lic'] = 'copyright'
				self.values['draft'] = True
				self.render('templates/item-edit.html')
		else:
			if x and draft:
				#check mandatory fields
				if not self.get_param('title') or not self.get_param('tags') or not self.get_param('description') or not self.get_param('content'):
					self.render_json({ 'saved': False })
					return
			if key:
				# update item
				item = model.Item.get(key)
				if not item:
					self.not_found()
					return
				if not user.nickname == item.author.nickname and user.rol != 'admin':
					self.forbidden()
					return
				
				lic = self.get_param('lic')
				lics = [license['id'] for license in licenses]
				if not lic in lics:
					lic = 'copyright'
				
				if not item.draft:
					self.delete_tags(item.tags)
				item.lic = lic
				item.tags = self.parse_tags(self.get_param('tags'))
				item.description = ' '.join(self.get_param('description').splitlines())
				item.content = self.get_param('content')
				if item.draft:
					# title and url_path can change only if the item hasn't already been published
					item.title = self.get_param('title')
					item.url_path = '%d/%s' % (item.key().id(), self.to_url_path(item.title))
				add_groups = False
				if item.draft and not draft:
					item.draft = draft
					user.items += 1
					user.draft_items -=1
					user.put()
					item.creation_date = datetime.datetime.now()
					
					app = model.Application.all().get()
					if app:
						app.items += 1
						app.put()
					memcache.delete('app')
					add_groups = True
				
				if not item.author_nickname:
					item.author_nickname = user.nickname
				
				if not item.content_html:	
					html = model.ItemHtml(content=self.markdown(item.content))
					html.put()
					item.content_html = html
				else:
					item.content_html.content = self.markdown(item.content)
					item.content_html.put()
				
				item.put()
				
				memcache.delete('index_items')
				memcache.delete('tag_cloud')
				memcache.delete(str(item.key().id()))
				
				if not draft:
					self.update_tags(item.tags)
				if x:
					self.render_json({ 'saved': True, 'key' : str(item.key()), 'updated' : True, "draft_items" : str(user.draft_items) })
				else:
					if add_groups:
						self.redirect('/item.add.groups?key=%s' % str(item.key()))
					else:
						self.redirect('/item/%s' % item.url_path)
			else:
				# new item
				today = datetime.date.today()
				title = self.get_param('title')
				tags = self.parse_tags(self.get_param('tags'))
				
				lic = self.get_param('lic')
				lics = [license['id'] for license in licenses]
				if not lic in lics:
					lic = 'copyright'
				
				item = model.Item(author=user,
					author_nickname=user.nickname,
					title=title,
					description=' '.join(self.get_param('description').splitlines()),
					content=self.get_param('content'),
					lic=lic,
					url_path='empty',
					tags=tags,
					draft=draft,
					item_type='article',
					views=0,
					responses=0,
					rating_count=0,
					rating_total=0,
					favourites=0)
				html = model.ItemHtml(content=self.markdown(item.content))
				html = model.ItemHtml(content=self.media_content(item.content))
				html.put()
				item.content_html = html
				item.subscribers = [user.email]
				item.put()
				
				self.add_user_subscription(user, 'item', item.key().id())
				item.url_path = '%d/%s' % (item.key().id(), self.to_url_path(item.title))
				item.put()
				
				memcache.delete('index_items')
				memcache.delete('tag_cloud')
				memcache.delete(str(item.key().id()))
				
				if not draft:
					user.items += 1
					user.put()
					self.update_tags(tags)
					self.add_follower(item=item, nickname=user.nickname)
					app = model.Application.all().get()
					if app:
						app.items += 1
						app.put()
						memcache.delete('app')
				else:
					user.draft_items += 1
					user.put()
				
				followers = list(self.get_followers(user=user))
				followers.append(user.nickname)
				self.create_event(event_type='item.new', followers=followers, user=user, item=item)
				
				if x:
					self.render_json({ 'saved': True, 'key' : str(item.key()), "updated" : False, "draft_items" : str(user.draft_items) })
				else:
					if item.draft:
						self.redirect('/item/%s' % item.url_path)
					else:
						self.redirect('/item.add.groups?key=%s' % str(item.key()))
