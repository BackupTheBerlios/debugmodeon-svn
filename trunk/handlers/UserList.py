#!/usr/bin/python
# -*- coding: utf-8 -*-

from handlers.BaseHandler import *

class UserList(BaseHandler):

	def execute(self):
		self.values['tab'] = '/'
		query = model.UserData.all().order('-creation_date')
		self.values['users'] = self.paging(query, 10)
		self.render('templates/user-list.html')
