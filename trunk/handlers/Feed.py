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