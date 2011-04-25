from google.appengine.ext import db

class Scrap(db.Model):
  owner = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  photo = db.BlobProperty(required=True)
  description = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(required=True, auto_now_add=True)
