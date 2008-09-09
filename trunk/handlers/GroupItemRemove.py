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

class GroupItemRemove(AuthenticatedHandler):

	def execute(self):
		item = model.Item.get(self.get_param('item'))
		group = model.Group.get(self.get_param('group'))
		if not item or not group:
			self.not_found()
			return
		
		gi = model.GroupItem.gql('WHERE group=:1 and item=:2', group, item).get()
		if self.values['user'].nickname == item.author.nickname:
			gi.delete()
			group.items -= 1
			group.put()
		self.redirect('/item/%s' % item.url_path)
