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

import wsgiref.handlers

import os
from handlers import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class NotAvailable(webapp.RequestHandler):

	def get(self):
		self.response.clear()
		self.response.set_status(501)
		self.response.headers['Content-Type'] = 'text/html;charset=UTF-8'
		self.response.headers['Pragma'] = 'no-cache'
		self.response.headers['Cache-Control'] = 'no-cache'
		self.response.headers['Expires'] = 'Wed, 27 Aug 2008 18:00:00 GMT'
		self.response.out.write(template.render('static/sorry.html', {}))

def main():
	application = webapp.WSGIApplication(
									   [('/.*', NotAvailable)],
									   debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()
