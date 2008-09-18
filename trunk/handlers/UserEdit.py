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

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class UserEdit(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']

		if method == 'GET':
			self.values['google_adsense'] = self.not_none(user.google_adsense)
			self.values['google_adsense_channel'] = self.not_none(user.google_adsense_channel)
			self.values['real_name'] = self.not_none(user.real_name)
			self.values['links'] = [(link.split('##', 2)[1], link.split('##', 2)[0]) for link in user.list_urls]
			self.values['country'] = self.not_none(user.country)
			self.values['city'] = self.not_none(user.city)
			self.values['about'] = self.not_none(user.about_user)
			self.render('templates/user-edit.html')
		else:
			user.google_adsense = self.get_param('google_adsense')
			user.google_adsense_channel = self.get_param('google_adsense_channel')
			user.real_name = self.get_param('real_name')
			user.country = self.get_param('country')
			image = self.request.get("img")
			if image:
				image = images.im_feeling_lucky(image, images.JPEG)
				user.avatar = img.resize(image, 128, 128)
				user.thumbnail = img.resize(image, 48, 48)
			user.city = self.get_param('city')
			user.list_urls = []
			blog = self.get_param('blog')
			if blog:
				user.list_urls.append(blog + '##blog')

			linkedin = self.get_param('linkedin')
			if linkedin:
				user.list_urls.append(linkedin + '##linkedin')
			user.about_user = self.get_param('about_user')
			user.put()
			self.redirect('/user/%s' % user.nickname)
	
	def not_none(self, value):
		if not value:
			return ''
		return value
		
		
		