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