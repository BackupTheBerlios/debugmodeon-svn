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

from handlers.AuthenticatedHandler import *

class GroupUserJoin(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		group = model.Group.get(self.get_param('group'))
		if not group:
			self.not_found()
			return
		
		if not self.auth():
			return
		
		redirect = self.get_param('redirect')
		
		gu = self.joined(group)
		if gu == 'False':
			self.create_group_subscribers(group)
			
			gu = model.GroupUser(user=user,
				group=group,
				user_nickname=user.nickname,
				group_title=group.title,
				group_url_path=group.url_path)
			gu.put()
			
			group.subscribers.append(user.email)
			group.members += 1
			if group.activity:
				group.activity += 1
			group.put()
			
			self.add_follower(group=group, nickname=user.nickname)
			
			self.add_user_subscription(user, 'group', group.key().id())
			user.groups += 1
			user.put()
		self.redirect(redirect)
