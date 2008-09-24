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

from django import template
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

import datetime

def relativize(value):
	now = datetime.datetime.now()
	diff = now - value
	days = diff.days
	seconds = diff.seconds
	if days > 365:
		return "%d años" % (days / 365, )
	if days > 30:
		return "%d meses" % (days / 30, )
	if days > 0:
		return "%d días" % (days, )
	
	if seconds > 3600:
		return "%d horas" % (seconds / 3600, )
	if seconds > 60:
		return "%d minutos" % (seconds / 60, )
		
	return "%d segundos" % (seconds, )
register.filter(relativize)

def nolinebreaks(value):
	return ' '.join(str(value).splitlines())
register.filter(nolinebreaks)

def markdown(value, arg=''):
	try:
		import markdown
	except ImportError:
		return "error"
	else:
		extensions=arg.split(",")
		return markdown.markdown(value, extensions, safe_mode=True)
register.filter(markdown)

def smiley(value):
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
	
	return value
register.filter(smiley)

class Pagination(template.Node):

	def render(self,context):
		prev = self.get('prev', context)
		next = self.get('next', context)
		params = []
		p = self.get('p', context)
		q = self.get('q', context)
		a = self.get('a', context)
		t = self.get('item_type', context)

		if a:
			a = '#%s' % str(a)
		else:
			a = ''

		if t:
			t = '&amp;item_type=%s' % str(t)
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
					s = '%s<a href="?%s%s%s">« anterior</a> |' % (s, qp, t, a)
				else:
					if q:
						qp = '&amp;q=%s' % str(q)
					else:
						qp = ''
					s = '%s<a href="?p=%d%s%s%s">« anterior</a> |' % (s, prev, qp, t, a)
			s = '%s Página %d ' % (s, p)
			if next:
				if q:
					q = '&amp;q=%s' % str(q)
				else:
					q = ''
				s = '%s| <a href="?p=%d%s%s%s">siguiente »</a>' % (s, next, q, t, a)
			s = '%s</p>' % s
		return s
	
	def get(self, key, context):
		try:
			return template.resolve_variable(key, context)
		except template.VariableDoesNotExist:
			return None


@register.tag
def pagination(parser, token):
	return Pagination()