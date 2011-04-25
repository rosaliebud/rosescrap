
import os
import logging

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
import jinja2
import facebook

import config
import model

# Setup jinja2 loader/env for HTMLHandler.render
loader = jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__),
                         'templates')])
env = jinja2.Environment(loader=loader, autoescape=False)

class Handler(webapp.RequestHandler):
  def get_fb_args(self):
    if not hasattr(self, 'fb_args'):
      self.fb_args = facebook.get_user_from_cookie(
          self.request.cookies, config.FACEBOOK_APP_ID,
          config.FACEBOOK_APP_SECRET)
    return self.fb_args

class HTMLHandler(Handler):
  values = {}

  def render(self, template_file_name):
    template = env.get_template(template_file_name)

    assert isinstance(self.values, dict)

    self.values['fb_app_id'] = config.FACEBOOK_APP_ID
    self.response.out.write(template.render(self.values))

class Index(HTMLHandler):
  def get(self):
    #grab 9 listings for the homepage
    listings_query = model.Scrap.all().order('-date')
    self.values['listings'] = listings_query.fetch(9)
    self.render('index.html')

class Listing(Handler):
  def post(self):
    fb_args = self.get_fb_args()
    if not fb_args or not fb_args['uid']:
      self.error(403)
      return

    photo = images.Image(self.request.get('Scrap_Photo'))
    photo.im_feeling_lucky()
    photo.resize(2000, 2000)
    photo = photo.execute_transforms(output_encoding=images.JPEG)

    scrap = model.Scrap(owner=fb_args['uid'],
                        name=self.request.get('Scrap_Name'),
                        photo=db.Blob(photo))
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
      if width > 2000:
        width = 2000
      img = images.Image(scrap.photo)
      img.resize(width=width, height=width)
      thumbnail = img.execute_transforms(output_encoding=images.JPEG)
      self.response.headers['Content-Type'] = 'image/jpeg'
      self.response.out.write(thumbnail)
      return
    self.error(404)

class Scrap (HTMLHandler):
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
