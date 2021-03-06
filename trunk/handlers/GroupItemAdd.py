#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
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
		
		if not self.auth():
			return
		
		user = self.values['user']
		gu = self.joined(group)
		if gu and not item.draft:
			gi = model.GroupItem.gql('WHERE group=:1 and item=:2', group, item).get()
			if not gi and user.nickname == item.author.nickname:
				gi = model.GroupItem(item=item,
					group=group,
					item_author_nickname=item.author_nickname,
					item_title=item.title,
					item_url_path=item.url_path,
					group_title=group.title,
					group_url_path=group.url_path)
				gi.put()
				
				group.items += 1
				if group.activity:
					group.activity += 15
				group.put()
				
				followers = list(self.get_followers(group=group))
				self.create_event(event_type='group.additem', followers=followers, user=user, group=group, item=item)
				
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
