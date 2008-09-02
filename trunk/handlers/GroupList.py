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
		query = model.Group.all().order('-creation_date')
		groups = self.paging(query, 10)
		for g in groups:
			g.items = model.GroupItem.all().filter('group =', g).count(1000)
			g.members = model.GroupUser.all().filter('group =', g).count(1000)
			g.put()
		self.values['groups'] = groups
		self.render('templates/group-list.html')
