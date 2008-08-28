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
from handlers.AuthenticatedHandler import *

class GroupForumReply(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		key = self.get_param('key')
		thread = model.Thread.get(key)
		group = thread.group

		response = model.ThreadResponse(thread=thread,
			author=user,
			content=self.get_param('content'))
		response.put()
		
		thread.responses = thread.responses + 1
		thread.put()
		
		group.responses = group.responses + 1
		group.put()

		self.redirect('/group.forum/%s#comments' % thread.url_path)