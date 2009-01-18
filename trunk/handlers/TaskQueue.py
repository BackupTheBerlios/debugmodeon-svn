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

import model
import simplejson

from google.appengine.ext import webapp

class TaskQueue(webapp.RequestHandler):

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain;charset=utf-8'
		
		task = model.Task.all().order('-priority').get()
		
		if not task:
			self.response.out.write('No pending tasks')
			return
		
		data = simplejson.loads(task.data)
		data = self.__class__.__dict__[task.task_type].__call__(self, data)
		
		if data is None:
			self.response.out.write('Task finished %s %s' % (task.task_type, task.data))
			task.delete()
		else:
			task.data = simplejson.dumps(data)
			task.put()
			self.response.out.write('Task executed but not finished %s %s' % (task.task_type, task.data))
	
	def delete_recommendations(self, data):
		offset = data['offset']
		recs = model.Recommendation.all().fetch(1, offset)
		if len(recs) == 0:
			return None

		next = recs[0]

		item_to   = next.item_to
		item_from = next.item_from
		if item_from.draft or item_to.draft or item_from.deletion_date is not None or item_to.deletion_date is not None:
			next.delete()
		else:
			data['offset'] += 1

		return data
		
	def begin_recommendations(self, data):
		offset = data['offset']
		items = model.Item.all().filter('draft', False).filter('deletion_date', None).order('creation_date').fetch(1, offset)
		print 'items: %d' % len(items)
		if len(items) == 0:
			return None

		next = items[0]
		data['offset'] += 1

		t = model.Task(task_type='item_recommendation', priority=0, data=simplejson.dumps({'item': next.key().id(), 'offset': 0}))
		t.put()

		return data
	
	def item_recommendation(self, data):
		
		def tanimoto(v1, v2):
			c1,c2,shr=0,0,0
			
			all = []
			all.extend(v1)
			all.extend(v2)
			
			l = len(all)
			shr = l - len(list(set(all)))
			
			c1 = len(v1)
			c2 = len(v2)
			
			return (float(shr) / float(c1+c2-shr))
		
		def create_recommendation(item_from, item_to, value):
			r = model.Recommendation.all().filter('item_from', item_from).filter('item_to', item_to).get()
			if not r:
				if not item_from.author_nickname:
					item_from.author_nickname = item_from.author.nickname
					item_from.put()
				r = model.Recommendation(item_from=item_from,
					item_to=item_to,
					value=value,
					item_from_title=item_from.title,
					item_to_title=item_to.title,
					item_from_author_nickname=item_from.author_nickname,
					item_to_author_nickname=item_to.author_nickname,
					item_from_url_path=item_from.url_path,
					item_to_url_path=item_to.url_path)
			elif r.value == value:
				return
			r.put()
		
		item = model.Item.get_by_id(data['item'])
		if item.draft or item.deletion_date is not None:
			return None
		offset = data['offset']
		
		items = model.Item.all().filter('draft', False).filter('deletion_date', None).order('creation_date').fetch(1, offset)
		if not items:
			return None
		
		next = items[0]
		data['offset'] += 1
		
		if next.key().id() != item.key().id():
			diff = tanimoto(item.tags, next.tags)
			if diff > 0:
				create_recommendation(item, next, diff)
				create_recommendation(next, item, diff)		
			
		return data
