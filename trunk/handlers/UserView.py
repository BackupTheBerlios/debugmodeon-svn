#!/usr/bin/python
# -*- coding: utf-8 -*-

from handlers.BaseHandler import *
from google.appengine.api import users

class UserView(BaseHandler):

	def execute(self):
		self.values['tab'] = '/'
		nickname = self.request.path.split('/', 2)[2]
		this_user = model.UserData.gql('WHERE nickname=:1', nickname).get()
		self.values['this_user'] = this_user
		query = model.Item.all().filter('author =', users.User(this_user.email)).order('-creation_date')
		self.values['items'] = self.paging(query, 10)
		self.render('templates/user-view.html')
