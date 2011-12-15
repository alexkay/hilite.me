# -*- coding: utf-8 -*-
#
# Copyright © 2009-2011 Alexander Kojevnikov <alexander@kojevnikov.com>
#
# hilite.me is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# hilite.me is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with hilite.me.  If not, see <http://www.gnu.org/licenses/>.

import os
import time
from email.utils import formatdate
from urllib import quote, unquote

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from tools import hilite_me, update_styles

class IndexHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')

        code = self.request.get('code')
        if not code:
            code = "print 'hello world!'"
        lexer = (self.request.get('lexer') or
                 unquote(self.request.cookies.get('lexer', '')))
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        style = (self.request.get('style') or
                 unquote(self.request.cookies.get('style', '')))
        styles = sorted(get_all_styles(), key=str.lower)
        linenos = (self.request.get('linenos') or
                   self.request.method == 'GET' and
                   unquote(self.request.cookies.get('linenos', ''))) or ''
        divstyles = self.request.get('divstyles',
                                     unquote(self.request.cookies.get('divstyles', '')))
        divstyles = update_styles(style, divstyles)

        html = hilite_me(code, lexer, style, linenos, divstyles)

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
