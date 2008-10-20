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
		comment_key = self.get_param('key')

		if method == 'GET':
			if comment_key:
				# show edit form
				comment = model.Comment.get(comment_key)
				if user.nickname != comment.author_nickname and user.rol != 'admin':
					self.forbidden()
					return
				if comment is None:
					self.not_found()
					return
				#TODO Check if it's possible
				self.values['comment'] = comment
				self.values['comment_key'] = comment.key
				self.render('templates/item-comment-edit.html')
				return
			else:
				self.error('Comentario no encontrado')
				return
		else:
			if comment_key:
				# update comment
				comment = model.Comment.get(comment_key)
				if user.nickname != comment.author_nickname and user.rol != 'admin':
					self.forbidden()
					return
					
				if not comment:
					self.not_found()
					return
				comment.content = self.get_param('content')
				if user.rol != 'admin':
					if comment.editions is None:
						comment.editions = 0
					comment.editions +=1
					comment.last_edition = datetime.datetime.now()
				comment.put()
				self.redirect('/item/%s/#comment-%s' % (comment.item.url_path, comment.response_number))
			else:
				self.error('Comentario no encontrado')
				return