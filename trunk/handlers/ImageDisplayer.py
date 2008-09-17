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

import logging
from handlers.BaseHandler import *

class ImageDisplayer(BaseHandler):
	def execute(self):
		params = self.request.path.split('/')
		if params[2] == 'user':
			user = model.UserData.gql('WHERE nickname=:1', params[4]).get()
			if not user:
				self.not_found()
				return

			if params[3] == 'avatar':
				self.showImage(user.avatar, 'user128.jpg')
			elif params[3] == 'thumbnail':
				self.showImage(user.thumbnail, 'user48.jpg')
		elif params[2] == 'group':
			logging.info('grupo')
			#item = model.Item.get_by_id(int(self.request.path.split('/')[2]))
			group = model.Group.get_by_id(int(params[4]))
			if not group:
				logging.info('no imagen')
				self.not_found()
				return
			if params[3] == 'avatar':
				self.showImage(group.avatar, 'glider128.png')
			elif params[3] == 'thumbnail':
				self.showImage(group.thumbnail, 'glider48.png')
		else:
			logging.info('else')
			self.not_found()
			return

	def showImage(self, image, default):
		if image:
			self.response.headers['Content-Type'] = 'image/jpg'
			self.response.out.write(image)
		else:
			self.redirect('/static/images/%s' % default)