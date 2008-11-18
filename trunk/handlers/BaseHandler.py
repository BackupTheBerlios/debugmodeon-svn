#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
# (C) Copyright 2008 Ignacio Andreu <plunchete at gmail dot com>
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte at gmail dot com>
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

import os
import re
import sha
import img
import model
import struct
import logging
import datetime
import simplejson

from utilities import session

from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.api import memcache

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from jinja2 import Template, Environment, FileSystemLoader

from google.appengine.runtime import apiproxy_errors

class BaseHandler(webapp.RequestHandler):

	def get_param(self, key):
		return self.get_unicode(self.request.get(key))

	def get_unicode(self, value):
		try:
			value = unicode(value, "utf-8")
		except TypeError:
			return value
		return value
		
	def create_jinja_environment(self):
		env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates' )))
		env.filters['relativize'] = self.relativize
		env.filters['markdown'] = self.markdown
		env.filters['smiley'] = self.smiley
		env.filters['pagination'] = self.pagination
		env.filters['media'] = self.media_content
		return env
	
	def get_template(self, env, f):
		p = f.split('/')
		if p[0] == 'templates':
			f = '/'.join(p[1:])
		t = env.get_template(f)
		return t
	
	def render_chunk(self, f, params):
		env = self.create_jinja_environment()
		t = self.get_template(env, f)
		return t.render(params)

	def render(self, f):
		self.response.headers['Content-Type'] = 'text/html;charset=UTF-8'
		self.response.headers['Pragma'] = 'no-cache'
		self.response.headers['Cache-Control'] = 'no-cache'
		self.response.headers['Expires'] = 'Wed, 27 Aug 2008 18:00:00 GMT'
		self.response.out.write(self.render_chunk(f, self.values))

	def relativize(self, value):
		now = datetime.datetime.now()
		try:
			diff = now - value
		except TypeError:
			return ''
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


	def markdown(self, value):
		try:
			import markdown
		except ImportError:
			return "error"
		else:
			return markdown.markdown(value, [], safe_mode='escape')
	
	def media_content(self,value):
		regex1 = re.compile('media=(.*);')
                match1 = regex1.search(value)
                if match1:
                        if re.match('(.*)youtube(.*)', match1.group(0)):
                                match2 = re.match('(.*)watch\?v=(\S+)', match1.group(1))
                                html = '<p><object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/%s"&hl=en&fs=1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s"=es&fs=1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object></p>' % ( match2.group(2), match2.group(2))
				value=value.replace(match1.group(0),html)
				return value

                        if re.match('(.*)vimeo(.*)', match1.group(0)):
                                match2 = re.match('(.*)vimeo.com/(\S+)',match1.group(1))
				html='<p><object width="400" height="300"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="300"></embed></object></p>' % ( match2.group(2), match2.group(2))		
				value=value.replace(match1.group(0),html)
				return value 
                return value 
	
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
		self.values['app'] = self.get_application()
		#self.values['activity_groups'] = self.groups_by_activity()
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
	
	def groups_by_activity(self):
		groups = model.Group.all().order('-activity').fetch(10)
		return groups
	
	def add_categories(self):
		cats = list(model.Category.all().order('title'))
		categories = {}
		for category in cats:
			# legacy code
			if not category.url_path:
				category.url_path = self.to_url_path(category.title)
				category.put()
			# end
			if category.parent_category is None:
				categories[str(category.key())] = category

		for category in cats:
			if category.parent_category is not None:
				parent_category = categories[str(category.parent_category.key())]
				if not parent_category.subcategories:
					parent_category.subcategories = []
				parent_category.subcategories.append(category)

		ret = [categories[key] for key in categories]
		ret.sort()
		self.values['categories'] = ret

	def add_tag_cloud(self):
		self.values['tag_cloud'] = self.cache('tag_cloud', self.get_tag_cloud)

	def get_tag_cloud(self):
		return self.tag_list(model.Tag.all().order('-count').fetch(30))
	
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
		p = p.encode('ascii', 'ignore')
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
		# logging.debug('looking for %s in the cache' % key)
		data = memcache.get(key)
		if data is not None:
			# logging.debug('%s is already in the cache' % key)
			return data
		else:
			data = function.__call__()
			# logging.debug('inserting %s in the cache' % key)
			memcache.add(key, data, timeout)
			return data
	
	"""
	def cache_this(self, function, timeout=600):
		key = '%s?%s' % (self.request.path, self.request.query)
		return self.cache(key, function, timeout)
	
	def pre_pag(self, query, max, default_order=None):
		try:
			p = int(self.get_param('p'))
		except ValueError:
			p = 1
		offset = (p-1)*max
		o = self.get_param('o')
		if o:
			query = query.order(o)
			self.values['o'] = o
		elif default_order:
			query = query.order(default_order)
		return [obj for obj in query.fetch(max+1, offset)]
		
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
		o = self.get_param('o')
		if o:
			self.values['o'] = o
		return a
	"""

	def paging(self, query, max, default_order=None, total=-1, accepted_orderings=[], key=None, timeout=300):
		if total > 0:
			pages = total / max
			if total % max > 0:
				pages += 1
			self.values['pages'] = pages
		try:
			p = int(self.get_param('p'))
		except ValueError:
			p = 1
		self.values['p'] = p
		offset = (p-1)*max
		#if offset > 1000:
		#	return None
		o = self.get_param('o')
		if o and o in accepted_orderings:
			query = query.order(o)
			self.values['o'] = o
		elif default_order:
			query = query.order(default_order)
		# caching
		if not key is None:
			a = memcache.get(key)
			if a is None:
				a = [obj for obj in query.fetch(max+1, offset)]
				memcache.add(key, a, timeout)
		else:
			a = [obj for obj in query.fetch(max+1, offset)]
		#
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

		s = ''
		if prev or next:
			params = []
			p = self.value('p')
			q = self.value('q')
			a = self.value('a')
			t = self.value('t')
			o = self.value('o')
			cat = self.value('cat')
			pages = self.value('pages')
			
			# order
			if cat:
				params.append('cat=%s' % cat)
   
			# query string
			if q:
				params.append('q=%s' % q)
   
			# type
			if t:
				params.append('t=%s' % t)
   
			# order
			if o:
				params.append('o=%s' % o)
   
			# anchor
			if a:
				a = '#%s' % str(a)
			else:
				a = ''

			common = '%s%s' % ('&amp;'.join(params), a)
			s = '<ul class="pagination">'
			if prev:
				if prev == 1:
					s = u'%s <li class="previous"><a href="?%s">« Anterior</a></li>' % (s, common)
				else:
					s = u'%s <li class="previous"><a href="?p=%d&amp;%s">« Anterior</a></li>' % (s, prev, common)
			else:
				s = u'%s <li class="previous-off">« Anterior</li>' % s
			
			if pages:
				i = 1
				while i <= pages:
					if i == p:
						s = u'%s <li class="active">%d</li>' % (s, i)
					else:
						s = u'%s <li><a href="?p=%d&amp;%s">%d</a></li>' % (s, i, common, i)
					i += 1
			else:
				s = u'%s <li class="active">Página %d </li>' % (s, p)
			if next:
				s = u'%s <li class="next"><a href="?p=%d&amp;%s">Siguiente »</a></li>' % (s, next, common)
			else:
				s = u'%s <li class="next-off">Siguiente »</li>' % s
			s = '%s</ul><br/><br/>' % s
		return s

	def value(self, key):
		try:
			return self.values[key]
		except KeyError:
			return None
	
	def mail(self, subject, body, to=[], bcc=[]):
		app = self.get_application()
		subject = "%s %s" % (app.mail_subject_prefix, subject)

		body = """
%s

%s
""" % (body,app.mail_footer)

		message = mail.EmailMessage(sender=app.mail_sender,
							subject=subject, body=body)
		if not to:
			message.to = app.mail_sender
		else:
			message.to = to
		
		if bcc:
			message.bcc = bcc
		try:
			message.send()
		except apiproxy_errors.OverQuotaError, message:
			# Record the error in your logs
			logging.error(message)
			
	def show_error(self, message):
		self.values['message'] = message
		self.render('templates/error.html')
		
	def add_user_subscription(self, user, subscription_type, subscription_id):
		user_subscription = model.UserSubscription(user=user,
			user_nickname=user.nickname,
			user_email=user.email,
			subscription_type=subscription_type,
			subscription_id=subscription_id,
			creation_date = datetime.datetime.now())
		subscription = model.UserSubscription.all().filter('user', user).filter('subscription_type', subscription_type).filter('subscription_id', subscription_id).get()
		if subscription is None:
			user_subscription.put()
			
	def remove_user_subscription(self, user, subscription_type, subscription_id):
		user_subscription = model.UserSubscription.all().filter('user', user).filter('subscription_type', subscription_type).filter('subscription_id', subscription_id).get()
		if user_subscription is not None:
			user_subscription.delete()
			
	def add_follower(self, object_type, object_id, nickname):
		follower = model.Follower.all().filter('object_type', object_type).filter('object_id', object_id).get()
		if follower:
			if nickname not in follower.followers:
				follower.followers.append(nickname)
				follower.put()
		else:
			follower = model.Follower(object_type=object_type,
				object_id=object_id,
				followers=[nickname])
			follower.put()
	
	def remove_follower(self, object_type, object_id, nickname):
		follower = model.Follower.all().filter('object_type', object_type).filter('object_id', object_id).get()
		if follower:
			if nickname in follower.followers:
				follower.followers.remove(nickname)
				follower.put()
