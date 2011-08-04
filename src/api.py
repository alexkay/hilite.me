# -*- coding: utf-8 -*-
#
# Copyright © 2009-2010 Alexander Kojevnikov <alexander@kojevnikov.com>
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

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from tools import hilite_me, update_styles

class ApiHandler(webapp.RequestHandler):
    def get(self):
        if self.request.get('code'):
            return self.post()

        path = os.path.join(os.path.dirname(__file__), 'templates/api.txt')
        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(template.render(path, {}))

    def post(self):
        code = self.request.get('code')
        lexer = self.request.get('lexer')
        style = self.request.get('style')
        linenos = self.request.get('linenos')
        divstyles = update_styles(style, self.request.get('divstyles'))

        html = hilite_me(code, lexer, style, linenos, divstyles)

        self.response.headers["Content-Type"] = "text/plain"
        self.response.out.write(html)
