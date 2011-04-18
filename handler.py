import os

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from model import *


class Listing(webapp.RequestHandler):
	def post(self):
		crap = Crap()
		
		crap.name = self.request.get('Stuff_Name')
		uploaded_file = self.request.body
		crap.description = self.request.get('Stuff_Description')
		crap.put()
		self.redirect('/')
		
	
class MainPage(webapp.RequestHandler):
	def get(self):
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(10)

		listings = Crap.all().fetch(10)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'

		template_values = {
			'greetings': greetings,
			'listings': listings,
			'url': url,
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
	def post(self):
		 greeting = Greeting()

		 if users.get_current_user():
			 greeting.author = users.get_current_user()

		 greeting.content = self.request.get('content')
		 greeting.put()
		 self.redirect('/')
