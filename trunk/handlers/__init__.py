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

from handlers.MainPage import *

# items
from handlers.ItemList import *
from handlers.ItemEdit import *
from handlers.ItemView import *
from handlers.ItemVote import *
from handlers.ItemDelete import *
from handlers.ItemComment import *
from handlers.ItemFavourite import *
from handlers.ItemCommentSubscribe import *
from handlers.ItemCommentDelete import *
from handlers.ItemAddGroups import *
from handlers.ItemCommentEdit import *
from handlers.ItemVisit import *

# users
from handlers.UserList import *
from handlers.UserView import *
from handlers.UserEdit import *
from handlers.UserItems import *
from handlers.UserLogin import *
from handlers.UserGroups import *
from handlers.UserLogout import *
from handlers.UserRegister import *
from handlers.UserChangePassword import *
from handlers.UserForgotPassword import *
from handlers.UserResetPassword import *
from handlers.UserDrafts import *
from handlers.UserContact import *
from handlers.UserFavourites import *
from handlers.UserContacts import *
from handlers.UserPromote import *
from handlers.UserEvents import *
from handlers.UserForums import *

# messages
from handlers.MessageEdit import *
from handlers.MessageSent import *
from handlers.MessageInbox import *
from handlers.MessageRead import *
from handlers.MessageDelete import *

# forums
from handlers.ForumList import *

# groups
from handlers.GroupList import *
from handlers.GroupEdit import *
from handlers.GroupView import *
from handlers.GroupMove import *
from handlers.GroupDelete import *
# group forums
from handlers.GroupForumList import *
from handlers.GroupForumEdit import *
from handlers.GroupForumView import *
from handlers.GroupForumReply import *
from handlers.GroupForumSubscribe import *
from handlers.GroupForumDelete import *
from handlers.GroupThreadEdit import *
from handlers.GroupForumMove import *
from handlers.GroupForumVisit import *
# group items
from handlers.GroupItemList import *
from handlers.GroupItemAdd import *
from handlers.GroupItemRemove import *

# group users
from handlers.GroupUserList import *
from handlers.GroupUserUnjoin import *
from handlers.GroupUserJoin import *

#search
from handlers.SearchResult import *

# inviting contacts
from handlers.Invite import *
# feed RSS
from handlers.Feed import *

from handlers.Tag import *
from handlers.Search import *

# images
from handlers.ImageDisplayer import *

# admin
from handlers.Admin import *
from handlers.AdminCategories import *
from handlers.AdminCategoryEdit import *
from handlers.AdminApplication import *
from handlers.GroupAddRelated import *
from handlers.AdminUsers import *
from handlers.MailQueue import *
from handlers.TaskQueue import *

from handlers.Apocalipto import *
from handlers.NotFound import *
from handlers.BaseRest import *

from handlers.Static import *
