#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import model
import simplejson

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class BaseHandler(webapp.RequestHandler):

	def get_param(self, key):
		return self.get_unicode(self.request.get(key))

	def get_unicode(self, value):
		try:
			value = unicode(value, "utf-8")
		except TypeError:
			return value
		return value

	def render(self, file):
		self.response.headers['Content-Type'] = 'text/html;charset=UTF-8'
		self.response.out.write(template.render(file, self.values))
	
	def render_json(self, data):
		self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
		self.response.out.write(simplejson.dumps(data))
	
	def pre_execute(self):
		self.execute()

	def get(self):
		self.common_stuff()
		self.pre_execute()
	
	def post(self):
		self.common_stuff()
		self.pre_execute()

	def common_stuff(self):
		self.values = {}
		self.values['redirect'] = '%s?%s' % (self.request.path, self.request.query)
		
		user = users.get_current_user()
		if user:
			self.values['user'] = user
			self.values['logout'] = users.create_logout_url(self.values['redirect'])
			
			user_data = model.UserData.gql('WHERE email=:1', user.email()).get()
			if not user_data:
				user_data = model.UserData(email=user.email(),
					nickname=user.nickname(),
					items=0,
					draft_items=0,
					messages=0,
					draft_messages=0,
					comments=0,
					rating_count=0,
					rating_total=0)
				user_data.put()
			self.values['user_data'] = user_data
		else:
			self.values['user'] = None
			self.values['login'] = users.create_login_url(self.values['redirect'])

	def to_url_path(self, value):
		value = value.lower()
		# table = maketrans(u'áéíóúÁÉÍÓÚñÑ', u'aeiouAEIOUnN')
		# value = value.translate(table)
		value = value.replace(u'á', 'a')
		value = value.replace(u'é', 'e')
		value = value.replace(u'í', 'i')
		value = value.replace(u'ó', 'o')
		value = value.replace(u'ú', 'u')
		value = value.replace(u'Á', 'A')
		value = value.replace(u'É', 'E')
		value = value.replace(u'Í', 'I')
		value = value.replace(u'Ó', 'O')
		value = value.replace(u'Ú', 'U')
		value = value.replace(u'ñ', 'n')
		value = value.replace(u'Ñ', 'N')
		value = '-'.join(re.findall('[a-zA-Z0-9]+', value))
		return value
	
	def unique_url_path(self, model, url_path):
		c = 1
		url_path_base = url_path
		while True:
			query = db.Query(model)
			query.filter('url_path =', url_path)
			count = query.count(1)
			if count > 0:
				url_path = '%s-%d' % (url_path_base, c)
				c = c + 1
				continue
			break
		return url_path
	
	def paging(self, query, max):
		try:
			p = int(self.get_param('p'))
		except ValueError:
			p = 1
		self.values['p'] = p
		if p > 1:
			self.values['prev'] = p-1
		offset = (p-1)*max
		a = [o for o in query.fetch(max+1, offset)]
		l = len(a)
		if l > max:
			self.values['len'] = max
			self.values['next'] = p+1
			return a[:max]
		self.values['len'] = l
		return a
	
	def delete_tags(self, tags):
		for tag in tags:
			t = model.Tag.gql('WHERE tag=:1', tag).get()
			if t:
				if t.count == 1:
					t.delete()
				else:
					t.count = t.count - 1
					t.put()
	
	def update_tags(self, tags):
		for tag in tags:
			t = model.Tag.gql('WHERE tag=:1', tag).get()
			if not t:
				tg = model.Tag(tag=tag,count=1)
				tg.put()
			else:
				t.count = t.count + 1
				t.put()
	
	def tag_list(self, tags):
		tagdict={}
		for t in tags:
			tagdict[t.tag] = t.count
		if not tagdict:
			return []
		maxcount = max(t.count for t in tags)
		taglist = [(tag, 6*tagdict[tag]/maxcount, tagdict[tag]) for tag in tagdict.keys()]
		taglist.sort()
		return taglist