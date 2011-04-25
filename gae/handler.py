import os
import logging

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
import jinja2

import model

# Setup jinja2 loader/env for Handler.render
loader = jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), 
                                               'templates')])
env = jinja2.Environment(loader=loader, autoescape=False)

class Handler(webapp.RequestHandler):
    values = {}
    
    def render(self, template_file_name):
        template = env.get_template(template_file_name)
        self.response.out.write(template.render(self.values))

class Index(Handler):
    def get(self):
        #grab 9 listings for the homepage
        listings_query = model.Scrap.all().order('-date')
        self.values['listings'] = listings_query.fetch(9) 
        self.render('index.html')

class Listing(webapp.RequestHandler):
    def post(self):
        scrap = model.Scrap()
        scrap.name = self.request.get('Scrap_Name')
        scrap.photo = db.Blob(self.request.get('Scrap_Photo'))
        scrap.description = self.request.get('Scrap_Description')
        scrap.put()
        self.redirect('/')

class ScrapImage(webapp.RequestHandler):
    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            self.error(404)
            return

        scrap = model.Scrap.get_by_id(id)
        if scrap and scrap.photo:
            width = self.request.get_range('w')
            if not width:
                width = 150
            img = images.Image(scrap.photo)
            img.resize(width=width, height=width)
            img.im_feeling_lucky()
            thumbnail = img.execute_transforms(output_encoding=images.JPEG)
            self.response.headers['Content-Type'] = 'image/jpeg'
            self.response.out.write(thumbnail)
            return
        self.error(404)

class Scrap (Handler):
    """Grab details and full image for Scrap item.
    """
    def get(self, id):
        try:
            id = int(id)
        except ValueError:
            self.error(404)
            return

        self.values['scrap'] = model.Scrap.get_by_id(id)
        self.render('scrap.html')
