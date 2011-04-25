from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import handler

mappings = [('/', handler.Index),
			('/list', handler.Listing),
			('/scrap/image/(.+)', handler.ScrapImage),
			('/scrap/(.+)', handler.Scrap)]

application = webapp.WSGIApplication(mappings, debug=True)

def main():
	 util.run_wsgi_app(application)

if __name__ == "__main__":
	 main()
