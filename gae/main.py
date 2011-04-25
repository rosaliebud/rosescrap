from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import handler

mappings = [('/', handler.Index),
			('/image', handler.FullImage),
			('/list', handler.Listing),
			('/scrappage', handler.ScrapPage),
			('/sign', handler.Guestbook),
			('/thumb', handler.Thumbnailer)]

application = webapp.WSGIApplication(mappings, debug=True)

def main():
	 util.run_wsgi_app(application)

if __name__ == "__main__":
	 main()
