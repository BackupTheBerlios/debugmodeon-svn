#!/usr/bin/python
# -*- coding: utf-8 -*-

from handlers.BaseHandler import *

class AuthenticatedHandler(BaseHandler):

	def pre_execute(self):
		user = self.values['user']
		if not user:
			self.redirect(self.values['login'])
			return
		self.execute()