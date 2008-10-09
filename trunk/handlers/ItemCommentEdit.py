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

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class ItemCommentEdit(AuthenticatedHandler):

	def execute(self):
		self.values['tab'] = '/item.list'
		method = self.request.method
		user = self.values['user']
		key = self.get_param('key')

		if method == 'GET':
			if key:
				# show edit form
				comment = model.Comment.get(key)
				"""user.nickname != comment.author_nickname and"""
				if user.rol != 'admin':
					self.forbidden()
					return
				if comment is None:
					self.not_found()
					return
				#TODO Check if it's possible
				self.values['comment'] = comment
				self.render('templates/item-comment-edit.html')
				return
			else:
				self.error('Comentario no encontrado')
				return
		else:
			if key:
				# update comment
				comment = model.Comment.get(key)
				if user.rol != 'admin':
					self.forbidden()
					return
				
				if not comment:
					self.not_found()
					return
				comment.content = self.get_param('content')
				comment.put()
				self.redirect('/item/%s' % (comment.item.url_path))
			else:
				self.error('Comentario no encontrado')
				return