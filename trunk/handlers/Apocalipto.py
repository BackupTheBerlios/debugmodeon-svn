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
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from handlers.BaseHandler import *

class Apocalipto(BaseHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		p = int(self.request.get('p'))
		key = self.request.get('key')
		action = self.request.get('action')
		group = model.Group.get(key)
		if not group:
			self.response.out.write('group not found')
			return
		
		offset = (p-1)*10
		if action == 'gi':
			i = self.group_items(group, offset)
		elif action == 'gu':
			i = self.group_users(group, offset)
		elif action == 'th':
			i = self.group_threads(group, offset)
		elif action == 'cc':
			i = self.contacts(offset)
		elif action == 'fv':
			i = self.favourites(offset)
		else:
			self.response.out.write('unknown action -%s-' % action)
			return
		self.response.out.write('Processed from %d to %d. %d updated. Action %s' % (offset, i[0], i[1], action))

	def group_items(self, group, offset):
		i = offset
		p = 0
		for gi in model.GroupItem.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not gi.group_title:
				item = gi.item
				group = gi.group
				gi.item_author_nickname = item.author_nickname
				gi.item_title = item.title
				gi.item_url_path = item.url_path
				gi.group_title = group.title
				gi.group_url_path = group.url_path
				gi.put()
				p += 1
			i+=1
		return (i, p)

	def group_users(self, group, offset):
		i = offset
		p = 0
		for gu in model.GroupUser.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not gu.group_title:
				user = gu.user
				group = gu.group
				gu.user_nickname = gu.user.nickname
				gu.group_title = group.title
				gu.group_url_path = group.url_path
				gu.put()
				p += 1
			i+=1
		return (i, p)

	def group_threads(self, group, offset):
		i = offset
		p = 0
		for th in model.Thread.all().filter('group', group).order('-creation_date').fetch(10, offset):
			if not th.group_title:
				group = th.group
				th.group_title = group.title
				th.group_url_path = group.url_path
				th.put()
				p += 1
			i+=1
		return (i, p)

	def contacts(self, offset):
		i = offset
		p = 0
		for cc in model.Contact.all().order('-creation_date').fetch(10, offset):
			if not cc.user_from_nickname:
				cc.user_from_nickname = cc.user_from.nickname
				cc.user_to_nickname = cc.user_to.nickname
				cc.put()
				p += 1
			i+=1
		return (i, p)

	def favourites(self, offset):
		i = offset
		p = 0
		for fv in model.Favourite.all().order('-creation_date').fetch(10, offset):
			if not fv.user_nickname:
				item = fv.item
				fv.item_author_nickname = item.author_nickname
				fv.item_title = item.title
				fv.item_url_path = item.url_path
				fv.user_nickname = fv.user.nickname
				fv.put()
				p += 1
			i+=1
		return (i, p)
