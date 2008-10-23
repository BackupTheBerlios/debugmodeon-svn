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

import datetime

from handlers.AuthenticatedHandler import *

class MessageDelete(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		key = self.request.get('key')
		message = model.Message.get(key)
		if not message:
			self.not_found()
			return
		
		if user.nickname == message.user_to_nickname:
			message.to_deletion_date = datetime.datetime.now()
			message.put()
			self.redirect('/message.inbox')
		elif user.nickname == message.user_from_nickname:
			message.from_deletion_date = datetime.datetime.now()
			message.put()
			self.redirect('/message.sent')
		else:
			self.forbidden()