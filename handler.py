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
		scrap = Scrap()
		
		scrap.name = self.request.get('Scrap_Name')
		scrap.photo = db.Blob(self.request.get('Scrap_Photo'))
		scrap.description = self.request.get('Scrap_Description')
		scrap.put()
		self.redirect('/')

class Thumbnailer(webapp.RequestHandler):
    def get(self):
        if self.request.get("id"):
            scrap = Scrap.get_by_id(int(self.request.get("id")))

            if scrap and scrap.photo:
                img = images.Image(scrap.photo)
                img.resize(width=160, height=160)
                img.im_feeling_lucky()
                thumbnail = img.execute_transforms(output_encoding=images.JPEG)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(thumbnail)
                return
				
		self.error(404)	
	
class FullImage(webapp.RequestHandler):
	def get(self):
		if self.request.get("id"):
			scrap = Scrap.get_by_id(int(self.request.get("id")))
		
			if scrap and scrap.photo:
				img = images.Image(scrap.photo)
				img.resize(width=500, height=500)
				img.im_feeling_lucky()
				fullsize = img.execute_transforms(output_encoding=images.JPEG)
		
				self.response.headers['Content-Type'] = 'image/jpeg'
		        self.response.out.write(fullsize)
		        return
		
		self.error(404)
		
class MainPage(webapp.RequestHandler):
	def get(self):
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(10)

#grab 9 listings for the homepage
		listings_query = Scrap.all().order('-date')
		listings = listings_query.fetch(9)
		#count = listings_query.cursor()
		#listings2 = listings_query.with_cursor(count)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'LOGOUT'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'LOGIN'

		template_values = {
			'greetings': greetings,
			#for the listing
			'listings': listings,
			'url': url,
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

#grab details and full image for scrappage
class ScrapPage (webapp.RequestHandler):
	def get(self):

		template_values = {
			'scrapdetail': Scrap.get_by_id(int(self.request.get('id')))
		}

		path = os.path.join(os.path.dirname(__file__), 'scrap.html')
		self.response.out.write(template.render(path, template_values))
		

class Guestbook(webapp.RequestHandler):
	def post(self):
		 greeting = Greeting()

		 if users.get_current_user():
			 greeting.author = users.get_current_user()

		 greeting.content = self.request.get('content')
		 greeting.put()
		 self.redirect('/')
