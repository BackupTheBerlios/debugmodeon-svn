#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Juan Luis Belmonte  <jlbelmonte at gmail dot com>
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

		if method == 'GET':
			if user.rol != 'admin':
				self.forbidden()
				return
			group_orig = model.Group.get(self.get_param('key_orig'))
			self.values['key_orig'] = group_orig.key
			self.render('templates/group-move.html')	
		else:
			if user.rol != 'admin':
				self.forbidden()
				return
			
			group_orig = model.Group.get(self.get_param('key_orig'))
			self.values['key_orig'] = group_orig.key
			
			try:
				group_dest = model.Group.get(self.get_param('key_dest'))
			except :
				self.render('templates/group-move-result.html')
				return

			for i in group_orig.groupitem_set:
				deleted=False	
				for j in group_dest.groupitem_set:
					if i.item.key() == j.item.key():
						i.delete()
						deleted=True
				if not deleted:
					i.group = group_dest
					group_dest.items +=1
					i.put()
								
			for i in group_orig.groupuser_set:
				deleted=False
				for j in group_dest.groupuser_set:
					if i.user.key() == j.user.key():
				 		i.delete()
						deleted=True
				if not deleted:
					i.group = group_dest
					group_dest.members +=1
					i.put()

			for i in group_orig.thread_set:
				i.group=group_dest
				group_dest.threads += 1
				i.put()
			
			group_dest.put()
			group_orig.delete()
			
			app = model.Application.all().get()		
			if app:
				app.groups -= 1
				app.put()
				memcache.delete('app')
			
			self.values['move_ok'] = True

			memcache.delete('index_groups')
			memcache.delete('index_threads')
		self.render('templates/group-move-result.html')	
	
