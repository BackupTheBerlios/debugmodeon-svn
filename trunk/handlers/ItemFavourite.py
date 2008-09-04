#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte@gmail.com> 
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

from google.appengine.ext import db
from handlers.AuthenticatedHandler import *

class ItemFavourite(AuthenticatedHandler):
	
	def execute(self):
		item = model.Item.get(self.get_param('key'))
		user = self.values['user']
	

		if not  model.Favourite.gql('WHERE user=:1 AND item=:2', user, item).get(): 
			favourite = model.Favourite(item=item,user=user)
			favourite.put()

			user.favourites += 1
			user.put()
		else:
			favourite =  model.Favourite.gql('WHERE user=:1 AND item=:2', user, item).get()
			favourite.delete()
                   	user.favourites -= 1
			user.put()
			
		
		self.redirect('/item/%s' % item.url_path)
