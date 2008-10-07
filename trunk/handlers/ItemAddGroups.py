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

class ItemAddGroups(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')
		item = model.Item.get(key)
		if not item or item.draft or item.deletion_date:
			self.not_found()
			return
		if not user.nickname == item.author.nickname:
			self.forbidden()
			return
		
		if method == 'GET':
			self.values['key'] = key
			self.values['item'] = item
			groups = list(model.GroupUser.all().filter('user', user).order('group_title'))
			self.values['groups'] = groups
			if not groups:
				self.redirect('/item/%s' % item.url_path)
				return
			self.render('templates/item-add-groups.html')
		else:
			arguments = self.request.arguments()
			for gu in model.GroupUser.all().filter('user', user).order('group_title'):
				group = gu.group
				if self.request.get('group-%d' % group.key().id()):
					gi = model.GroupItem.all().filter('group', group).filter('item', item).count(1)
					if not gi:
						gi = model.GroupItem(group=group,
							item=item,
							item_author_nickname = item.author_nickname,
							item_title = item.title,
							item_url_path = item.url_path,
							group_title = group.title,
							group_url_path = group.url_path)
						gi.put()
			self.redirect('/item/%s' % item.url_path)