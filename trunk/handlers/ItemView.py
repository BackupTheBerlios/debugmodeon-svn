#!/usr/bin/python
# -*- coding: utf-8 -*-

from google.appengine.ext import db
from handlers.BaseHandler import *

class ItemView(BaseHandler):

	def execute(self):
		url_path = self.request.path.split('/', 2)[2]
		item = model.Item.gql('WHERE url_path=:1', url_path).get()
		user = self.values['user']
		if not user or item.author != user:
			item.views = item.views + 1
			item.put()
		
		self.values['item'] = item
		query = model.Comment.all().filter('item =', item).order('creation_date')
		self.values['comments'] = self.paging(query, 10)
		self.values['url_path'] = url_path
		self.render('templates/item-view.html')