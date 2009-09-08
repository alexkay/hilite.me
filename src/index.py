import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from pygments.lexers import get_all_lexers

class IndexHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        self.response.out.write(template.render(path, {'lexers': lexers}))
