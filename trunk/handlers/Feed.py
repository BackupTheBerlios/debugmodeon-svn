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

import time
import model
import datetime
import markdown

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from time import strftime, gmtime, time

class Feed(webapp.RequestHandler):

	def get(self):
		data = memcache.get(self.request.path)
		if not data:
			params = self.request.path.split('/', 3)
   
			if params[2] == 'tag':
				query = model.Item.all().filter('deletion_date', None).filter('tags =', params[3]).order('-creation_date')
				latest = [o for o in query.fetch(10)]
				data = self.to_rss(u'Artículos etiquetados con %s' % params[3], latest)
   
			elif params[2] == 'group.forum':
				group = model.Group.gql('WHERE url_path=:1',params[3]).get()
				if not group:
					group = model.Group.gql('WHERE old_url_path=:1',params[3]).get()
				threads = model.Thread.gql('WHERE group=:1 ORDER BY creation_date DESC LIMIT 20', group)
				data = self.threads_to_rss(u'Foro %s' % group.title, threads)
   
			elif params[2] == 'group':
				group = model.Group.gql('WHERE url_path=:1',params[3]).get()
				if not group:
					group = model.Group.gql('WHERE old_url_path=:1',params[3]).get()
				group_items = model.GroupItem.gql('WHERE group=:1 ORDER BY creation_date DESC LIMIT 20', group)
				latest = [gi.item for gi in group_items]
				data = self.to_rss(u'Artículos del grupo %s' % group.title, latest)
   
			elif params[2] == 'user':
				#user = model.UserData.gql('WHERE nickname=:1', params[3]).get()
				latest = model.Item.gql('WHERE author_nickname=:1 AND draft=:2 AND deletion_date=:3 ORDER BY creation_date DESC LIMIT 20', params[3], False, None)
				data = self.to_rss(u'Artículos de %s' % params[3], latest)
   
			elif not params[2]:
				latest = model.Item.gql('WHERE draft=:1 AND deletion_date=:2 ORDER BY creation_date DESC LIMIT 20', False, None)
				data = self.to_rss('debug_mode=ON', latest)
				
			else:
				self.not_found()
				return
				
			memcache.add(self.request.path, data, 600)
			
		self.response.headers['Content-Type'] = 'application/rss+xml'
		self.response.out.write(template.render('templates/feed.xml', data))
		
	
	def threads_to_rss(self, title, threads):
		items = []
		url = self.get_application().url
		md = markdown.Markdown()
		for i in threads:
			item = {
				'title': i.title,
				'link': "%s/group.forum/%s" % (url, i.url_path),
				'description': md.convert(i.content),
				'pubDate': self.to_rfc822(i.creation_date),
				'guid':"%s/group.forum/%s" % (url,i.url_path),
				'author': i.author_nickname
				# guid como link para mantener compatibilidad con feed.xml
			}
			items.append(item)

		values = {
			'title': title,
			'self': url+self.request.path,
			'link': url,
			'description': '',
			'items': items
		}
		return values

	def to_rss(self, title, latest):
		import MediaContentFilters as contents
		items = []
		url = self.get_application().url
		md = markdown.Markdown()
		for i in latest:
			if i.author.not_full_rss:
				content = md.convert(i.description)
			else:
				content = md.convert(i.content)
				content = contents.media_content(content)
			item = {
				'title': i.title,
				'link': "%s/item/%s" % (url, i.url_path),
				'description': content,
				'pubDate': self.to_rfc822(i.creation_date),
				'guid':"%s/item/%d/" % (url, i.key().id()),
				'author': i.author_nickname
				
			}
			items.append(item)
			
		values = {
			'title': title,
			'self': url+self.request.path,
			'link': url,
			'description': '',
			'items': items
		}
		return values
	
	def to_rfc822(self, date):
		return date.strftime("%a, %d %b %Y %H:%M:%S GMT")
		
	def get_application(self):
		app = memcache.get('app')
		import logging
		if not app:
			app = model.Application.all().get()
			memcache.add('app', app, 0)
		return app
