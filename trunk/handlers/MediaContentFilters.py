#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) Copyright 2008 Juan Luis Belmonte <jlbelmonte at gmail dot com>
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

import re
#main method to apply all filters

def media_content(value):
    if re.search('youtube',value):
        value=youtube(value)
    if re.search('vimeo', value):
        value=vimeo(value)
    if re.search('slideshare', value):
        value=slideshare(value)
    
    return value

# specific methods for the different services

def youtube(text):
    targets = re.findall('media=http://www.youtube.com/watch\?v=\S+;', text)
    for i in targets:
        match= re.match('(.*)watch\?v=(\S+);',i)
        html = '<p><object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/%s"&hl=en&fs=1"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/%s"=es&fs=1" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="425" height="344"></embed></object></p>' % ( match.group(2), match.group(2))
        text=text.replace(i,html)
    return text

def vimeo(text):
    targets = re.findall('media=\S*vimeo.com/\S+;',text)
    for i in targets:
        match = re.match('(\S*)vimeo.com/(\S+)',i)
        html='<p><object width="400" height="300"><param name="allowfullscreen" value="true" /><param name="allowscriptaccess" value="always" /><param name="movie" value="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" /><embed src="http://vimeo.com/moogaloop.swf?clip_id=%s&amp;server=vimeo.com&amp;show_title=1&amp;show_byline=1&amp;show_portrait=0&amp;color=&amp;fullscreen=1" type="application/x-shockwave-flash" allowfullscreen="true" allowscriptaccess="always" width="400" height="300"></embed></object></p>' % ( match.group(2), match.group(2))
        text=text.replace(i,html)
    return text

def slideshare(text):
    targets = re.findall('(media=\[.*\];)', text)    
    for i in targets:
	match = re.search('id=(.*)&doc=(.*)&w=(.*)',i)
	html = '<p><div style="width:425px;text-align:left" id="__ss_%s"><object style="margin:0px" width="%s" height="355"><param name="movie" value="http://static.slideshare.net/swf/ssplayer2.swf?doc=%s"/><param name="allowFullScreen" value="true"/><param name="allowScriptAccess" value="always"/><embed src="http://static.slideshare.net/swf/ssplayer2.swf?doc=%s" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="%s" height="355"/></object></div></p>' %(match.group(1),match.group(3),match.group(2),match.group(2),match.group(3))
        text = match.group(0)
	#text=text.replace(i,html)
    return  text



#print media_content('''q
#slide media=[slideshare id=776832&doc=billy-cripe-visual-resume-1227332474087406-9&w=425];
#media=http://www.youtube.com/watch?v=j2lEk1NJwz4;
#
#media=http://www.vimeo.com/173714;
#ddddddds''')

