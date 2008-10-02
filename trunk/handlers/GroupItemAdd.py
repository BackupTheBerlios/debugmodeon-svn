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

import logging
from google.appengine.api import mail
from handlers.AuthenticatedHandler import *
from google.appengine.runtime import apiproxy_errors

class GroupItemAdd(AuthenticatedHandler):

	def execute(self):
		item = model.Item.get(self.get_param('item'))
		group = model.Group.get(self.get_param('group'))
		if not group or not item or item.draft or item.deletion_date:
			self.not_found()
			return
		user = self.values['user']
		gu = self.joined(group)
		if gu and not item.draft:
			gi = model.GroupItem.gql('WHERE group=:1 and item=:2', group, item).get()
			if not gi and user.nickname == item.author.nickname:
				gi = model.GroupItem(item=item, group=group)
				gi.put()
				
				self.create_group_subscribers(group)
				group.items += 1
				group.put()
				
				subscribers = group.subscribers
				if subscribers and user.email in subscribers:
					subscribers.remove(user.email)
					
				if subscribers:
					app = self.get_application()
					subject = u"Nuevo articulo: '%s'" % self.clean_ascii(item.title)
   
					body = u"""
Nuevo articulo en el grupo %s.
Titulo del articulo: %s
Leelo en esta direccion:
%s/item/%s

""" % (self.clean_ascii(group.title), self.clean_ascii(item.title), app.url, item.url_path)
					self.mail(subject=subject, body=body, bcc=group.subscribers)
				
		self.redirect('/item/%s' % item.url_path)
