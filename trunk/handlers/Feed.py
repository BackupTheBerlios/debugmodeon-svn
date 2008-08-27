#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import markdown
from handlers.BaseHandler import *
from time import strftime, gmtime, time

class Feed(BaseHandler):

	def execute(self):
		latest = model.Item.gql('ORDER BY creation_date DESC LIMIT 20')
		items = []
		url = 'http://debugmodeon.com'
		md = markdown.Markdown()
		for i in latest:
			item = {
				'title': i.title,
				'link': "%s/item/%s" % (url, i.url_path),
				'description': '<![CDATA[%s]]>' % (md.convert(i.description), ),
				'pubDate': self.to_rfc822(i.creation_date)
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