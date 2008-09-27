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

import re
import sha
import model
import simplejson
import datetime
import img

import struct

from utilities import session
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import images

class BaseHandler(webapp.RequestHandler):

	def get_param(self, key):
		return self.get_unicode(self.request.get(key))

	def get_unicode(self, value):
		try:
			value = unicode(value, "utf-8")
		except TypeError:
			return value
		return value

	def render(self, f):
		import os
		from jinja2 import Template, Environment, FileSystemLoader

		env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates' )))
		env.filters['relativize'] = self.relativize
		env.filters['markdown'] = self.markdown
		env.filters['smiley'] = self.smiley
		env.filters['pagination'] = self.pagination
		p = f.split('/')
		if p[0] == 'templates':
			f = '/'.join(p[1:])
		t = env.get_template(f)
		
		self.response.headers['Content-Type'] = 'text/html;charset=UTF-8'
		self.response.headers['Pragma'] = 'no-cache'
		self.response.headers['Cache-Control'] = 'no-cache'
		self.response.headers['Expires'] = 'Wed, 27 Aug 2008 18:00:00 GMT'
		self.response.out.write(t.render(self.values))

	def relativize(self, value):
		now = datetime.datetime.now()
		diff = now - value
		days = diff.days
		seconds = diff.seconds
		if days > 365:
			return u"%d años" % (days / 365, )
		if days > 30:
			return u"%d meses" % (days / 30, )
		if days > 0:
			return u"%d días" % (days, )
   
		if seconds > 3600:
			return u"%d horas" % (seconds / 3600, )
		if seconds > 60:
			return u"%d minutos" % (seconds / 60, )
   
		return u"%d segundos" % (seconds, )
		
	def smiley(self, value):
		"""
		value = value.replace(' :)', ' <img src="/static/images/smileys/smile.png" class="icon" alt=":)" />')
		value = value.replace(' :-)', ' <img src="/static/images/smileys/smile.png" class="icon" alt=":-)" />')
   
		value = value.replace(' :D', ' <img src="/static/images/smileys/jokingly.png" class="icon" alt=":D" />')
		value = value.replace(' :-D', ' <img src="/static/images/smileys/jokingly.png" class="icon" alt=":-D" />')
   
		value = value.replace(' :(', ' <img src="/static/images/smileys/sad.png" class="icon" alt=":(" />')
		value = value.replace(' :-(', ' <img src="/static/images/smileys/sad.png" class="icon" alt=":-(" />')
   
		value = value.replace(' :|', ' <img src="/static/images/smileys/indifference.png" class="icon" alt=":|" />')
		value = value.replace(' :-|', ' <img src="/static/images/smileys/indifference.png" class="icon" alt=":-|" />')
   
		value = value.replace(' :O', ' <img src="/static/images/smileys/surprised.png" class="icon" alt=":O" />')
		value = value.replace(' :/', ' <img src="/static/images/smileys/think.png" class="icon" alt=":/" />')
		value = value.replace(' :P', ' <img src="/static/images/smileys/tongue.png" class="icon" alt=":P" />')
		value = value.replace(' :-P', ' <img src="/static/images/smileys/tongue.png" class="icon" alt=":-P" />')
   
		value = value.replace(' ;)', ' <img src="/static/images/smileys/wink.png" class="icon" alt=";)" />')
		value = value.replace(' ;-)', ' <img src="/static/images/smileys/wink.png" class="icon" alt=";-)" />')
   
		value = value.replace(' :*)', ' <img src="/static/images/smileys/embarrassed.png" class="icon" alt=":*)" />')
		value = value.replace(' 8-)', ' <img src="/static/images/smileys/cool.png" class="icon" alt="8-)" />')
   
		# value = value.replace(' :'(', ' <img src="/static/images/smileys/cry.png" class="icon" alt=":'(" />')
		value = value.replace(' :_(', ' <img src="/static/images/smileys/cry.png" class="icon" alt=":_(" />')
   
		value = value.replace(' :-X', ' <img src="/static/images/smileys/crossedlips.png" class="icon" alt=":-X" />')
		"""
		return value


	def markdown(self, value, arg=''):
		try:
			import markdown
		except ImportError:
			return "error"
		else:
			extensions=arg.split(",")
			return markdown.markdown(value, extensions, safe_mode=True)
	
	def render_json(self, data):
		self.response.headers['Content-Type'] = 'application/json;charset=UTF-8'
		self.response.headers['Pragma'] = 'no-cache'
		self.response.headers['Cache-Control'] = 'no-cache'
		self.response.headers['Expires'] = 'Wed, 27 Aug 2008 18:00:00 GMT'
		self.response.out.write(simplejson.dumps(data))
	
	def pre_execute(self):
		self.execute()

	def get(self):
		self.common_stuff()
		self.pre_execute()
	
	def post(self):
		self.common_stuff()
		self.pre_execute()

	def get_current_user(self):
		try:		
			userKey = self.sess['user_key']
			user = db.get(userKey)
			return user
		except KeyError:
			return None

	def common_stuff(self):
		self.sess = session.Session()
		self.values = {}
		self.values['sess'] = self.sess
		redirect = '%s?%s' % (self.request.path, self.request.query)
		self.values['redirect'] = redirect
		
		user = self.get_current_user()
		# user = users.get_current_user()
		if user:
			self.values['logout'] = '/user.logout?redirect_to=%s' % redirect  # users.create_logout_url(self.values['redirect'])
			"""
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
					rating_total=0,
					rating_average=0,
					threads=0,
					responses=0,
					groups=0,
					favourites=0,
					public=False)
				user_data.put()
			self.values['user'] = user_data
			"""
			self.values['user'] = user
		else:
			self.values['user'] = None
			self.values['login'] = '/user.login?redirect_to=%s' % redirect # users.create_login_url(self.values['redirect'])

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
	
	def clean_ascii(self, value):
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
		value = ' '.join(re.findall('[a-zA-Z0-9()_\.:;-]+', value))
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
	
	def delete_tags(self, tags):
		tags=set(tags)
		for tag in tags:
			t = model.Tag.gql('WHERE tag=:1', tag).get()
			if t:
				if t.count == 1:
					t.delete()
				else:
					t.count = t.count - 1
					t.put()
	
	def update_tags(self, tags):
		tags=set(tags)
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

	def add_tag_cloud(self):
		self.values['tag_cloud'] = self.cache('tag_cloud', self.get_tag_cloud)

	def get_tag_cloud(self):
		return self.tag_list(model.Tag.all())
	
	# I use strings in order to distinguish three values into the templates
	# 'True', 'False', and None
	def joined(self, group):
		gu = model.GroupUser.gql('WHERE group=:1 and user=:2', group, self.values['user']).get()
		if gu is not None:
			return 'True'
		return 'False'
	
	def parse_tags(self, tag_string):
		tags = [self.to_url_path(t) for t in tag_string.split(',')]
		return list(set(tags))

	def hash(self, login, p, times=100):
		p = '%s:%s' % (login, p)
		for i in range(0, times):
			p = sha.new(p).hexdigest()
		return p
	
	"""
	def handle_exception(self, exception, debug_mode):
		self.response.clear()
		self.response.set_status(500)
		
		self.render('templates/error500.html')
	"""

	def not_found(self):
		self.response.clear()
		self.response.set_status(404)

		self.render('templates/error404.html')
	
	def is_contact(self, this_user):
		user = self.values['user']
		if not user:
			return False
		if model.Contact.all().filter('user_from', user).filter('user_to', this_user).get():
			return True
		return False

	def create_group_subscribers(self, group):	
		if not group.subscribers:
			com = [g.user.email for g in model.GroupUser.all().filter('group', group).fetch(1000) ]
			group.subscribers = list(set(com))

	def cache(self, key, function, timeout=0):
		data = memcache.get(key)
		if data is not None:
			return data
		else:
			data = function.__call__()
			memcache.add(key, data, timeout)
			return data
	
	def cache_this(self, function, timeout=600):
		key = '%s?%s' % (self.request.path, self.request.query)
		return self.cache(key, function, timeout)
	
	def pre_pag(self, query, max):
		try:
			p = int(self.get_param('p'))
		except ValueError:
			p = 1
		offset = (p-1)*max
		return [o for o in query.fetch(max+1, offset)]
		
	def post_pag(self, a, max):
		try:
			p = int(self.get_param('p'))
		except ValueError:
			p = 1
		self.values['p'] = p
		if p > 1:
			self.values['prev'] = p-1
		l = len(a)
		if l > max:
			self.values['len'] = max
			self.values['next'] = p+1
			return a[:max]
		self.values['len'] = l
		return a
		
	def can_write(self, group):
		if group.all_users is None or group.all_users:
			return True
		user = self.values['user']
		if not user:
			return False
		if model.GroupUser.all().filter('group', group).filter('user', user).get():
			return True
		return False
			
	def paging(self, query, max):
		a = self.pre_pag(query, max)
		return self.post_pag(a, max)
	
	def check_password(self, user, password):
		times = 100
		user_password = user.password
		s = user.password.split(':')
		if len(s) > 1:
			times = int(s[0])
			user_password = s[1]

		return self.hash(user.nickname, password, times) == user_password
	
	def hash_password(self, nickname, password):
		times = 5
		return '%d:%s' % (times, self.hash(nickname, password, times))
	
	def get_application(self):
		return self.cache('app', self.fetch_application)
	
	def fetch_application(self):
		return model.Application.all().get()

	def not_none(self, value):
		if not value:
			return ''
		return value

	def pagination(self, value):
		prev = self.value('prev')
		next = self.value('next')
		params = []
		p = self.value('p')
		q = self.value('q')
		a = self.value('a')
		t = self.value('t')

		if a:
			a = '#%s' % str(a)
		else:
			a = ''

		if t:
			t = '&amp;t=%s' % str(t)
		else:
			t = ''

		s = ''
		if prev or next:
			s = '<p class="pagination">'
			if prev:
				if prev == 1:
					if q:
						qp = 'q=%s' % str(q)
					else:
						qp = ''
					s = u'%s<a href="?%s%s%s">« anterior</a> |' % (s, qp, t, a)
				else:
					if q:
						qp = '&amp;q=%s' % str(q)
					else:
						qp = ''
					s = u'%s<a href="?p=%d%s%s%s">« anterior</a> |' % (s, prev, qp, t, a)
			s = u'%s Página %d ' % (s, p)
			if next:
				if q:
					q = '&amp;q=%s' % str(q)
				else:
					q = ''
				s = u'%s| <a href="?p=%d%s%s%s">siguiente »</a>' % (s, next, q, t, a)
			s = '%s</p>' % s
		return s

	def value(self, key):
		try:
			return self.values[key]
		except KeyError:
			return None