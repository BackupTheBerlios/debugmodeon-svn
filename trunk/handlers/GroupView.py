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

from google.appengine.ext import db
from handlers.BaseHandler import *

class GroupView(BaseHandler):

	def execute(self):
		self.values['tab'] = '/group.list'
		url_path = self.request.path.split('/', 2)[2]
		group = model.Group.gql('WHERE url_path=:1', url_path).get()
		if not group:
			group = model.Group.gql('WHERE old_url_path=:1', url_path).get()
			if group:
				self.redirect('/group/%s' % group.url_path, permanent=True)
				return
			self.not_found()
			return

		self.values['group'] = group
		self.values['joined'] = self.joined(group)
		self.values['items'] = list(model.GroupItem.all().filter('group', group).order('-creation_date').fetch(5))
		self.values['threads'] = list(model.Thread.all().filter('group', group).filter('parent_thread', None).order('-last_response_date').fetch(5))
		self.values['users'] = list(model.GroupUser.all().filter('group', group).order('-creation_date').fetch(5))
		self.values['related'] = list(model.RelatedGroup.all().filter('group_from', group).order('-creation_date').fetch(10))
		self.render('templates/group-view.html')