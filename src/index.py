import os
import time
from email.utils import formatdate
from urllib import quote, unquote

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

class IndexHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')

        code = self.request.get('code')
        if not code:
            code = "print 'hello world!'"
        lexer = (self.request.get('lexer') or
                 unquote(self.request.cookies.get('lexer', '')))
        if not lexer:
            lexer = 'python'
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        style = (self.request.get('style') or
                 unquote(self.request.cookies.get('style', '')))
        if not style:
            style = 'colorful'
        styles = sorted(get_all_styles(), key=str.lower)
        linenos = (self.request.get('linenos') or
                   self.request.method == 'GET' and
                   unquote(self.request.cookies.get('linenos', ''))) or ''
        divstyles = self.request.get('divstyles',
                                     unquote(self.request.cookies.get('divstyles', '')))
        if not divstyles:
            divstyles = 'color:black;background:white;border:solid grey;'
            divstyles += 'border-width:.1em .1em .1em .8em;padding:.2em .6em;'
        defstyles = 'overflow:auto;width:auto;'
        formatter = HtmlFormatter(style=style,
                                  linenos='inline' if linenos else False,
                                  noclasses=True,
                                  cssclass='',
                                  cssstyles=defstyles + divstyles,
                                  prestyles='margin: 0')
        html = highlight(code, get_lexer_by_name(lexer), formatter)
        html = "<!-- HTML generated using hilite.me -->\n" + html
        next_year = formatdate(time.time() + 60*60*24*365)
        self.response.headers.add_header('Set-Cookie',
                                         'lexer=%s; expires=%s' %
                                         (quote(lexer), next_year))
        self.response.headers.add_header('Set-Cookie',
                                         'style=%s; expires=%s' %
                                         (quote(style), next_year))
        self.response.headers.add_header('Set-Cookie',
                                         'linenos=%s; expires=%s' %
                                         (quote(linenos), next_year))
        self.response.headers.add_header('Set-Cookie',
                                         'divstyles=%s; expires=%s' %
                                         (quote(divstyles), next_year))
        self.response.out.write(template.render(path, locals()))

    post = get
