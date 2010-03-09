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
from google.appengine.ext.webapp.util import run_wsgi_app

from index import IndexHandler
from api import ApiHandler

debug = os.environ.get('SERVER_SOFTWARE', '').lower().startswith('devel');
if debug:
    import logging
    logging.logMultiprocessing = 0

application = webapp.WSGIApplication([('/', IndexHandler),
                                      ('/api', ApiHandler),
                                     ],
                     debug=debug)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
