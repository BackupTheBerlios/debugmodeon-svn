#!/usr/bin/python
# -*- coding: utf-8 -*-

from handlers.BaseHandler import *

class MainPage(BaseHandler):

	def execute(self):
		self.values['tab'] = '/'
		query = model.Item.all().order('-creation_date')
		self.values['items'] = self.paging(query, 10)
		self.values['taglist'] = self.tag_list(model.Tag.all())
		self.render('templates/index.html')
