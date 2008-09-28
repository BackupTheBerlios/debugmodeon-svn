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

class GroupDelete(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		
		if user.rol != 'admin':
			self.forbidden()
			return 

		group=model.Group.get(self.get_param('key'))
		db.delete(group.groupuser_set)
		db.delete(group.groupitem_set)
		db.delete(group.thread_set)
		group.delete()

		app = self.get_application()
                if app:
			app.groups -=1
                        app.put()
	

		self.redirect('/')
