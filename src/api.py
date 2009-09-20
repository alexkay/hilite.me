import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from tools import hilite_me, update_styles

class ApiHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/api.txt')
        self.response.headers.add_header("Content-Type", "text/plain")
        self.response.out.write(template.render(path, {}))

    def post(self):
        code = self.request.get('code')
        lexer = self.request.get('lexer')
        style = self.request.get('style')
        linenos = self.request.get('linenos')
        divstyles = update_styles(style, self.request.get('divstyles'))

        html = hilite_me(code, lexer, style, linenos, divstyles)

        self.response.headers.add_header("Content-Type", "text/plain")
        self.response.out.write(html)
