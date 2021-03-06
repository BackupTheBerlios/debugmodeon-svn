#!/usr/bin/python
# -*- coding: utf-8 -*-

#
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

import datetime

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class ItemDeleteComment(AuthenticatedHandler):

	def execute(self):
		user = self.values['user']
		if user.rol != 'admin':
			self.forbidden()
			return
		
		comment = model.Comment.get(self.get_param('key'))
		url = comment.item.url_path
		if not comment:
			self.not_found()
			return
		

		#decrement number of comments in the Item
		comment.item.responses -= 1
		comment.item.put()
		#decrement nomber of comments in the User
		comment.author.comments -= 1
		comment.author.put()
			
		#delete comment
		comment.delete()
		self.redirect('/item/%s' % url)
