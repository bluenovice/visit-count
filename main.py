#a simple program to check a no of times a user has visited a site using cookies

import webapp2
import jinja2
import os
import hmac
from google.appengine.ext import db


#loading of jina environment starts from here
template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape= True)

#making hash function 
#here md5 algo is used
Secret_value = "unknown_cookie_values_present_here_so_that_it_remains_secret"
def hash_str(s):
	return hmac.new(Secret_value,s).hexdigest()

#making a secure value which returns a turple  of type (s,has_str)
#where hash str is a hash value of a string
def make_secure_val(s):
	return "%s-%s"%(s,hash_str(s))

def check_secure_val(h):
	val = h.split('-')[0]
	if h == make_secure_val(val):
		return val


class Handler(webapp2.RequestHandler):
	def write(self,*a , **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainHandler(Handler):
		def get(self):
			self.response.headers['Content-Type'] = 'text/plain'
			visits =0
			visit_cookie_str = self.request.cookies.get('visit')

			if visit_cookie_str:
				cookie_val = check_secure_val(visit_cookie_str)
				if cookie_val:
					visits = int(cookie_val)
			visits += 1

			new_cookie_val = make_secure_val(str(visits))

			self.response.headers.add_header('Set-Cookie' , 'visit = %s' % new_cookie_val)

			if visits >100:
				self.write("you are the one of best ")
			else:
				self.write("you have been visited the site for %s times " %visits)



app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)