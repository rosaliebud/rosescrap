from google.appengine.ext import db

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Scrap(db.Model):
	name = db.StringProperty()
	photo = db.BlobProperty()
	description = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)
	