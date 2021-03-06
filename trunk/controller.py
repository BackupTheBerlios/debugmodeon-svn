#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# (C) Copyright 2008 Alberto Gimeno <gimenete at gmail dot com>
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

import wsgiref.handlers

from handlers import *

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

# webapp.template.register_template_library('django.contrib.markup.templatetags.markup')
webapp.template.register_template_library('templatefilters')

def main():
	application = webapp.WSGIApplication(
									   [('/', MainPage),
									   # items
									   ('/item.list',				ItemList),
									   ('/item.edit',				ItemEdit),
									   ('/item.favourite',			ItemFavourite),
									   ('/item.vote',				ItemVote),
									   ('/item/.*',					ItemView),
									   ('/item.comment.subscribe',	ItemCommentSubscribe),
									   ('/item.comment',			ItemComment),
									   ('/item.delete',				ItemDelete),
									   ('/item.comment.delete',		ItemCommentDelete),
									   ('/item.add.groups',			ItemAddGroups),
									   ('/item.comment.edit',		ItemCommentEdit),
									   ('/item.visit',				ItemVisit),
									   # users
									   ('/user.list',			UserList),
									   ('/user/.*',				UserView),
									   ('/user.edit',			UserEdit),
									   ('/user.register',		UserRegister),
									   ('/user.login',			UserLogin),
									   ('/user.logout',			UserLogout),
									   ('/user.changepassword',	UserChangePassword),
									   ('/user.forgotpassword',	UserForgotPassword),
									   ('/user.resetpassword',	UserResetPassword),
									   ('/user.drafts',			UserDrafts),
									   ('/user.items/.*',		UserItems),
									   ('/user.groups/.*',		UserGroups),
									   ('/user.favourites/.*',	UserFavourites),
									   ('/user.contacts/.*',	UserContacts),
									   ('/user.contact',		UserContact),
									   ('/user.promote',			UserPromote),
									   ('/user.events',			UserEvents),
									   ('/user.forums/.*',		UserForums),
									   # messages
									   ('/message.edit',		MessageEdit),
									   ('/message.sent',		MessageSent),
									   ('/message.inbox',		MessageInbox),
									   ('/message.read/.*',		MessageRead),
									   ('/message.delete',		MessageDelete),
									   # forums,
									   ('/forum.list',			ForumList),
									   # groups
									   ('/group.list',	GroupList),
									   ('/group.edit',	GroupEdit),
									   ('/group.move',	GroupMove),
									   ('/group.delete',	GroupDelete),
									   ('/group/.*',	GroupView),
									   # group forums
									   ('/group.forum.list/.*',	GroupForumList),
									   ('/group.forum.edit',	GroupForumEdit),
									   ('/group.forum/.*',		GroupForumView),
									   ('/group.forum.reply',	GroupForumReply),
									   ('/group.forum.subscribe',	GroupForumSubscribe),
									   ('/group.forum.delete',	GroupForumDelete),
									   ('/group.thread.edit',	GroupThreadEdit),
									   ('/group.forum.move',	GroupForumMove),
									   ('/group.forum.visit',	GroupForumVisit),
									   # group items
									   ('/group.item.list/.*',	GroupItemList),
									   ('/group.item.add',		GroupItemAdd),
									   ('/group.item.remove',	GroupItemRemove),
									   # group users
									   ('/group.user.list/.*',	GroupUserList),
									   ('/group.user.unjoin',	GroupUserUnjoin),
									   ('/group.user.join',		GroupUserJoin),
									   # inviting contacts
									   ('/invite',			Invite),
									   # rss
									   ('/feed/.*', Feed),
									   
									   ('/tag/.*', Tag),
									   ('/search', Search),
									   ('/search.result', SearchResult),
									   # images
									   ('/images/.*', ImageDisplayer),
									   # admin
									   ('/admin', 				Admin),
									   ('/admin.application',	AdminApplication),
									   ('/admin.categories',	AdminCategories),
									   ('/admin.category.edit',	AdminCategoryEdit),
									   ('/group.add.related',	GroupAddRelated),
									   ('/admin.users',			AdminUsers),
									   ('/mail.queue',			MailQueue),
									   ('/task.queue',			TaskQueue),
									
									   ('/apocalipto', 	Apocalipto),
									   ('/html/.*', 	Static),
									   ('/.*', 			NotFound)],
									   debug=True)
	wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
	main()
