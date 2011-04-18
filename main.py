from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handler import *

application = webapp.WSGIApplication([('/', MainPage),
	                                  ('/sign', Guestbook),
									('/thumb', Thumbnailer),
									('/list', Listing)],
	                                 debug=True)

def main():
	 run_wsgi_app(application)

if __name__ == "__main__":
	 main()
