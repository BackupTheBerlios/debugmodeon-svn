import os
import sha
import time
import Cookie

COOKIE_NAME = 'dmo'

class Session(object):

	def __init__(self, seed):
		self.time  = None
		self.user  = None
		self.auth  = None
		self.seed  = seed
	
	def load(self):
		string_cookie = os.environ.get('HTTP_COOKIE', '')
		# string_cookie = 'dmo="1229551142;gimenete;9d5027fdb5f50aa35771bcd2eb12dc260a99f9cc"; expires=Wed, 17-Dec-2008 21:59:02 GMT; Path=/; HttpOnly'
		self.cookie = Cookie.SimpleCookie()
		self.cookie.load(string_cookie)
		if self.cookie.get(COOKIE_NAME):
			value  = self.cookie[COOKIE_NAME].value
			tokens = value.split(';')
			if len(tokens) != 3:
				return False
			else:
				h = tokens[2]
				tokens = tokens[:-1]
				tokens.append(self.seed)
				if h == self.hash(tokens):
					self.time = tokens[0]
					self.user = tokens[1]
					self.auth = h
					t = int(self.time) # TODO: catch
					if t > int(time.time()):
						# print self.cookie
						return True
		return False
	
	def store(self, user, expire):
		self.time = str(int(time.time())+expire)
		self.user = user
		params = [self.time, self.user, self.seed]
		self.auth = self.hash(params)
		params = [self.time, self.user, self.auth]
		self.cookie[COOKIE_NAME] = ';'.join(params)
		self.cookie[COOKIE_NAME]['expires'] = expire
		print self.cookie
	
	def hash(self, params):
		return sha.new(';'.join(params)).hexdigest()
	
	"""
	def __str__(self):	
		params = [self.time, self.user, self.auth]
		self.cookie[COOKIE_NAME] = ';'.join(params)
		self.cookie[COOKIE_NAME]['path'] = '/'
		return self.cookie.output()
	"""

"""
s = Session('1234')
if s.load():
	print s.auth
	print s.user
s.store('gimenete', 3200)
print s
"""