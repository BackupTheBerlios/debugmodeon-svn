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

class GroupAddRelated(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		self.values['tab'] = '/admin'

		if user.rol != 'admin':
			self.forbidden()
			return

		if method == 'GET':
			self.values['m'] = self.get_param('m')
			self.render('templates/group-add-related.html')
		else:
			group_from = model.Group.get_by_id(int(self.request.get('group_from')))
			group_to = model.Group.get_by_id(int(self.request.get('group_to')))
			
			related = model.RelatedGroup.all().filter('group_from', group_from).filter('group_to', group_to).get()
			if related:
				self.redirect('/group.add.related?m=Already_exists')
				return
			
			self.create_related(group_from, group_to)
			self.create_related(group_to, group_from)
			
			self.redirect('/group.add.related?m=Updated')
	
	def create_related(self, group_from, group_to):
		related = model.RelatedGroup(group_from = group_from,
			group_to = group_to,
			group_from_title = group_from.title,
			group_from_url_path = group_from.url_path,
			group_to_title = group_to.title,
			group_to_url_path = group_to.url_path)
		related.put()