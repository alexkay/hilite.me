import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from index import IndexHandler

debug = os.environ.get('SERVER_SOFTWARE', '').lower().startswith('devel');
if debug:
    import logging
    logging.logMultiprocessing = 0

application = webapp.WSGIApplication([('/', IndexHandler),
                                     ],
                     debug=debug)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
