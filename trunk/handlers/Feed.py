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
import datetime
import markdown
from handlers.BaseHandler import *
from time import strftime, gmtime, time

class Feed(BaseHandler):

	def execute(self):

		params = self.request.path.split('/')
		
		if params[2]=='tag':
			query = model.Item.all().filter('tags =', params[3]).order('-creation_date')
			latest = self.paging(query,20)
			self.to_rss(latest)
			self.to_rss(latest)
		elif params[2] == 'group.forum':
                       group = model.Group.gql('WHERE title=:1',params[3]).get()
                       threads = model.Thread.gql('WHERE group=:1 ORDER BY creation_date DESC LIMIT 20', group)
                       self.threads_to_rss(threads)	
		
		
		elif  params[2]=='group':
			group = model.Group.gql('WHERE title=:1',params[3]).get()
			group_items = model.GroupItem.gql('WHERE group=:1 ORDER BY creation_date DESC LIMIT 20',group)
			latest = [gi.item for gi in group_items]
			
			self.to_rss(latest)
		        
		elif params[2]=='user':
		        user = model.UserData.gql('WHERE nickname=:1', params[3]).get()
			latest = model.Item.gql('WHERE author=:1 AND draft=:2 ORDER BY creation_date DESC LIMIT 20',user,False)
			self.to_rss(latest)
	
		elif not params[2]:
			latest = model.Item.gql('WHERE draft=:1 ORDER BY creation_date DESC LIMIT 20', False)
			self.to_rss(latest)
	
	def threads_to_rss(self,threads):

                items = []
		url = 'http://debugmodeon.com'
                md = markdown.Markdown()
                for i in threads:
                        item = {
                                'title': i.title,
                                'link': "%s/group.forum/%s" % (url,i.url_path),
                                'description': '<![CDATA[%s]]>' % (md.convert(i.content), ),
                                'pubDate': self.to_rfc822(i.creation_date),
				'guid':"%s/group.forum/%s" % (url,i.url_path)
				# guid como link para mantener compatibilidad con feed.xml
                        }
                        items.append(item)

                values = {
                        'title': 'debug_mode=ON',
                        'self': url+'/feed',
                        'link': url,
                        'description': '',
                        'items': items
                }
                self.response.headers['Content-Type'] = 'application/rss+xml'
                self.response.out.write(template.render('templates/feed.xml', values))



	def to_rss(self,latest):	

		items = []
		url = 'http://debugmodeon.com'
		md = markdown.Markdown()
		for i in latest:
			item = {
				'title': i.title,
				'link': "%s/item/%s" % (url, i.url_path),
				'description': '<![CDATA[%s]]>' % (md.convert(i.description), ),
				'pubDate': self.to_rfc822(i.creation_date),
				'guid':"%s/item/%d/" % (url, i.key().id())
			}
			items.append(item)
			
		values = {
			'title': 'debug_mode=ON',
			'self': url+'/feed',
			'link': url,
			'description': '',
			'items': items
		}
		self.response.headers['Content-Type'] = 'application/rss+xml'
		self.response.out.write(template.render('templates/feed.xml', values))
	
	def to_rfc822(self, date):
		return date.strftime("%a, %d %b %Y %H:%M:%S GMT")
