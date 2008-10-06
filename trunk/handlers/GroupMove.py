#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Juan Luis Belmonte  <jlbelmonte at gmail dot com>
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
from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class GroupMove(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		if user.rol != 'admin':
			self.forbidden()
			return
			
		if method == 'GET':
			action = self.get_param('action')
			key = self.get_param('key_orig')
			if key:
				group_orig = model.Group.get(key)
				self.values['key_orig'] = group_orig.key
			self.render('templates/group-move.html')
			return
		else:
			action = action = self.get_param('action')
			if not action:
				self.render('templates/group-move.html')
				return
			key_orig = self.get_param('key_orig')
			if key_orig:
				group_orig = model.Group.get(key_orig)
			key_dest = self.get_param('key_dest')
			if key_dest:
				group_dest = model.Group.get(key_dest)
			mesagge = ''
			if not group_orig:
				message = 'No existe el grupo origen'
				self.values['message'] = message
				self.render('templates/group-move.html')
				return
			elif not group_dest:
				message = 'No existe el grupo destino'
				self.values['message'] = message
				self.render('templates/group-move.html')
				return
			elif action == 'mu':
				#move users
				message = self.move_users(group_orig, group_dest)
			elif action == 'mt':
				#move threads
				message = self.move_threads(group_orig, group_dest)
				memcache.delete('index_threads')
			elif action == 'mi':
				#move items
				message = self.move_items(group_orig, group_dest)
			elif action == 'delete':
				message = self.delete_group(group_orig)
				memcache.delete('index_groups')
			if action != 'delete':
				self.values['key_orig'] = group_orig.key
				self.values['key_dest'] = group_dest.key
			self.values['message'] = message
			self.render('templates/group-move.html')
			return 
	
	def move_items(self, group_orig, group_dest):
		group_items = model.GroupItem.all().filter('group', group_orig).fetch(10)
		counter = 0
		for group_item in group_items:
			item_dest = model.GroupItem.all().filter('group', group_dest).filter('item', group_item.item).get()
			if item_dest:
				group_item.delete()
				group_orig.items -= 1
				group_orig.put()
			else:
				group_item.group = group_dest
				group_item.group_title = group_dest.title
				group_item.group_url_path = group_dest.url_path
				group_item.put()
				group_dest.items += 1
				group_dest.put()
				counter +=1
		
		return 'Movidos %s items. Quedan %s en el grupo origen.' % (counter, group_orig.items)
		
	def move_threads(self, group_orig, group_dest):
		group_thread = model.Thread.all().filter('group', group_orig).filter('parent_thread', None).fetch(1)[0]
		group_thread.group = group_dest
		group_thread.group_url_path = group_dest.url_path
		group_thread.group_title = group_dest.title
		responses = model.Thread.all().filter('parent_thread', group_thread)
		counter = 0
		if responses:
			for response in responses:
				response.group = group_dest
				response.group_url_path = group_dest.url_path
				response.group_title = group_dest.title
				response.put()
				counter +=1
		
		group_thread.put()
		group_orig.threads -= 1
		group_orig.put()
		group_dest.threads += 1
		group_dest.put()
		return 'Movido un hilo con %s comentarios. Quedan %s hilos.' % (counter, group_orig.threads)
		
		
	def move_users(self, group_orig, group_dest):
		group_users = model.GroupUser.all().filter('group', group_orig).fetch(10)
		counter = 0
		for group_user in group_users:
			user_dest = model.GroupUser.all().filter('group', group_dest).filter('user', group_user.user).get()
			if user_dest:
				group_user.user.groups -= 1
				group_user.user.put()
				group_user.delete()
			else:
				group_user.group = group_dest
				group_dest.members += 1
				group_dest.subscribers.append(group_user.user.email)
				group_dest.put()
				counter += 1
				group_user.group_title = group_dest.title
				group_user.group_url = group_dest.url_path
				group_user.put()
			
			group_orig.members -= 1
			group_orig.put()

		return 'Movidos %s usuarios. Quedan %s en el grupo origen.' % (counter, group_orig.members)
	
	def delete_group(self, group_orig):
		group_orig.delete()
		app = model.Application.all().get()
		if app:
			app.groups -= 1
			app.put()
			memcache.delete('app')
		return 'Grupo borrado. Existen %s grupos.' % (app.groups)
