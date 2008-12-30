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

from google.appengine.api import mail 
from google.appengine.ext import db
from handlers.BaseHandler import *
import re
class Invite(BaseHandler):
	
	def execute(self):
		user = self.values['user']
		method = self.request.method
	
		if not user:
			
                        self.redirect('/user.login')
		
		if method == 'GET':
		        self.values['personalmessage']="""Te invito a visitar debug_mode=ON, una red social y de contenidos sobre el mundo informatico.
	                	%s	 
                        """  % self.get_application().url 
			self.render('templates/invite-friends.html')
			return
		elif self.auth():
			
			contacts = self.get_param('contacts').replace(' ','')
			contacts = contacts.rsplit(',',19)
			if contacts[0]=='' or not contacts:
				self.values['failed']=True
				self.render('templates/invite-friends.html')
				return
			self.values['_users'] = []
			
			
			invitations = []
			for contact in contacts:
				#FIXME inform the user about bad formed mails
				if re.match('\S+@\S+\.\S+', contact):
					u = model.UserData.gql('WHERE email=:1', contact).get()
					if u:
						self.values['_users'].append(u) 
					else:
						invitations.append(contact)
				
			personalmessage =  self.get_param('personalmessage')
			subject = " %s te invita a participar en debug_mode=ON" % user.nickname  
			body = """
	Te invito a visitar debug_mode=ON, una red social y de contenidos sobre el mundo informatico.
	
	http://www.debugmodeon.com	 
	"""   
			if personalmessage:

				body="""%s \n\n\n\n\t http://www.debugmodeon.com
					"""  % self.clean_ascii(personalmessage)
			self.mail(subject=subject, body=body, bcc=invitations)
	 		
			self.values['sent'] = True
			self.render('templates/invite-friends.html')

