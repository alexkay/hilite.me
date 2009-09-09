import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from pygments import highlight
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

class IndexHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')

        code = self.request.get("code")
        if not code:
            # read from cookies
            code = "print 'hello world!'"
        lexer = self.request.get("lexer")
        if not lexer:
            lexer = "python"
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        style = self.request.get("style")
        if not style:
            style = "colorful"
        styles = sorted(get_all_styles(), key=str.lower)

        formatter = HtmlFormatter(style=style,
                                  noclasses=True,
                                  cssclass='',
                                  cssstyles=
                                  "overflow:auto;"
                                  "width:auto;"
                                  "border:solid#959596;"
                                  "border-width:.1em .1em .1em .8em;"
                                  "padding:.2em .6em;",
                                  prestyles="margin: 0")
        html = highlight(code, get_lexer_by_name(lexer), formatter)
        self.response.out.write(template.render(path, locals()))

    def post(self):
        self.get() 
