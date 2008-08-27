#!/usr/bin/python
# -*- coding: utf-8 -*-

import wsgiref.handlers

from handlers import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

webapp.template.register_template_library('django.contrib.markup.templatetags.markup')

def main():
	application = webapp.WSGIApplication(
									   [('/', MainPage),
									   ('/item.list', ItemList),
									   ('/item.edit', ItemEdit),
									   ('/item/.*', ItemView),
									   ('/item.comment', ItemComment),
									   ('/user.list', UserList),
									   ('/user/.*', UserView),
									   ('/feed/', Feed)],
									   debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()