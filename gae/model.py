from google.appengine.ext import db

class Scrap(db.Model):
	name = db.StringProperty()
	photo = db.BlobProperty()
	description = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
