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

class MessageRead(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		url_path = self.request.path.split('/', 2)[2]
		message = model.Message.gql('WHERE url_path=:1', url_path).get()
		if message.user_to_nickname != user.nickname:
			self.forbidden()
			return
		
		if not message.read:
			message.read = True
			message.put()
			user.unread_messages -= 1
			user.put()
		
		self.values['message'] = message
		self.render('templates/message-read.html')