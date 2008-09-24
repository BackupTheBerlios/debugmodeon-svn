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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class Apocalipto(webapp.RequestHandler):

	def get(self):
		"""
		self.kill(model.Item.all())
		self.kill(model.Comment.all())
		self.kill(model.UserData.all())
		self.kill(model.GroupItem.all())
		self.kill(model.GroupUser.all())
		self.kill(model.Group.all())
		self.kill(model.Tag.all())
		self.kill(model.Thread.all())
		self.kill(model.ThreadResponse.all())
		"""
		self.redirect('/')
	
	def kill(self, all):
		for l in all:
			l.delete()
