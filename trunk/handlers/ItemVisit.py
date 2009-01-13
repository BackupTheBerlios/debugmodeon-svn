#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Ignacio Andreu <plunchete at gmail dot com>
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

from handlers.BaseRest import *

class ItemVisit(BaseRest):

	def get(self):
		item_id = self.request.get('id')
				
			
		memcache.delete(item_id + '_item')
		item = model.Item.get_by_id(int(item_id))
		item.views += 1
		item.put()
		memcache.add(str(item.key().id()) + '_item', item, 0)
		content = []
		self.render_json({'views' : item.views})
		return