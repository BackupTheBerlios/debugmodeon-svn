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

from handlers.AuthenticatedHandler import *

class AdminApplication(AuthenticatedHandler):

	def execute(self):
		method = self.request.method
		user = self.values['user']
		self.values['tab'] = '/admin'
		
		if user.rol != 'admin':
			self.forbidden()
			return
		
		if method == 'GET':
			app = self.get_application()
			self.values['m'] = self.get_param('m')
			if not app:
				app = model.Application()
			self.values['app'] = app
			self.values['url'] = self.not_none(app.url)
			self.values['mail_subject_prefix'] = self.not_none(app.mail_subject_prefix)
			self.values['mail_sender'] = self.not_none(app.mail_sender)
			self.values['mail_footer'] = self.not_none(app.mail_footer)
			self.values['recaptcha_public_key'] = self.not_none(app.recaptcha_public_key)
			self.values['recaptcha_private_key'] = self.not_none(app.recaptcha_private_key)
			self.values['google_adsense'] = self.not_none(app.google_adsense)
			self.values['google_adsense_channel'] = self.not_none(app.google_adsense_channel)
			self.values['max_results'] = self.not_none(app.max_results)
			self.values['max_results_sublist'] = self.not_none(app.max_results_sublist)
			self.render('templates/admin-application.html')
		elif self.auth():
			app = self.get_application()
			if not app:
				app = model.Application()
				app.users	= model.UserData.all().count()
				app.groups	= model.Group.all().count()
				app.threads = model.Thread.all().filter('parent_thread', None).count()
				app.items	= model.Item.all().filter('draft =', False).filter('deletion_date', None).count()
			app.url						= self.get_param('url')
			app.mail_subject_prefix		= self.get_param('mail_subject_prefix')
			app.mail_sender				= self.get_param('mail_sender')
			app.mail_footer				= self.get_param('mail_footer')
			app.recaptcha_public_key	= self.get_param('recaptcha_public_key')
			app.recaptcha_private_key	= self.get_param('recaptcha_private_key')
			app.google_adsense			= self.get_param('google_adsense')
			app.google_adsense_channel	= self.get_param('google_adsense_channel')
			if self.get_param('max_results'):
				app.max_results	= int(self.get_param('max_results'))
			if self.get_param('max_results_sublist'):
				app.max_results_sublist	= int(self.get_param('max_results_sublist'))
			app.put()
			memcache.delete('app')
			self.redirect('/admin.application?m=Updated')