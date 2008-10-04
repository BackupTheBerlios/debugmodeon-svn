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

from handlers.BaseHandler import *
from google.appengine.api import users

class UserView(BaseHandler):

	def execute(self):
		self.values['tab'] = '/user.list'
		nickname = self.request.path.split('/', 2)[2]
		this_user = model.UserData.gql('WHERE nickname=:1', nickname).get()
		if not this_user:
			self.not_found()
			return
		# TODO: not show if the user profile is not public
		user = self.values['user']
		contact = False
		if user and user.nickname != this_user.nickname:
			self.values['canadd'] = True
			contact = self.is_contact(this_user)
			self.values['is_contact'] = contact
		if (user is not None and this_user.nickname == user.nickname) or contact:
			self.values['im_addresses'] = [(link.split('##', 2)[1], link.split('##', 2)[0]) for link in this_user.im_addresses]
		else:
			self.values['im_addresses'] = []
		self.values['this_user'] = this_user
		links = [(link.split('##', 2)[1], link.split('##', 2)[0]) for link in this_user.list_urls]
		self.values['links'] = links
		self.values['personal_message'] = this_user.personal_message
		self.values['items'] = model.Item.all().filter('author =', this_user).filter('draft =', False).filter('deletion_date', None).order('-creation_date').fetch(5)
		self.values['groups'] = [gi.group for gi in model.GroupUser.all().filter('user =', this_user).order('-creation_date').fetch(5)]
		self.values['contacts'] = model.Contact.all().filter('user_from', this_user).order('-creation_date').fetch(5)
		self.render('templates/user-view.html')
