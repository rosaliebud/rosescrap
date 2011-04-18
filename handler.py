import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.api import images
from google.appengine.ext import db

from model import *


class Listing(webapp.RequestHandler):
	def post(self):
		crap = Crap()
		
		crap.name = self.request.get('Crap_Name')
		crap.photo = db.Blob(self.request.get('Crap_Photo'))
		crap.description = self.request.get('Crap_Description')
		crap.put()
		self.redirect('/')

class Thumbnailer(webapp.RequestHandler):
    def get(self):
        if self.request.get("id"):
            crap = Crap.get_by_id(int(self.request.get("id")))

            if crap and crap.photo:
                img = images.Image(crap.photo)
                img.resize(width=160, height=160)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return
				
		self.error(404)	
	
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
