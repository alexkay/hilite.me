#!/usr/bin/env python
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

import datetime
from urllib import quote_plus, unquote_plus

from flask import Flask, make_response, render_template, request

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from tools import *


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index_handler():
        code = request.form.get('code', "print 'hello world!'")
        lexer = (
            request.form.get('lexer', '') or
            unquote_plus(request.cookies.get('lexer', '')))
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        style = (
            request.form.get('style', '') or
            unquote_plus(request.cookies.get('style', '')))
        styles = sorted(get_all_styles(), key=str.lower)
        linenos = (
            request.form.get('linenos', '') or
            request.method == 'GET' and
            unquote_plus(request.cookies.get('linenos', ''))) or ''
        divstyles = request.form.get(
            'divstyles', unquote_plus(request.cookies.get('divstyles', '')))
        divstyles = update_styles(style, divstyles)

        html = hilite_me(code, lexer, style, linenos, divstyles)
        response = make_response(render_template('index.html', **locals()))

        next_year = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie('lexer', quote_plus(lexer), expires=next_year)
        response.set_cookie('style', quote_plus(style), expires=next_year)
        response.set_cookie('linenos', quote_plus(linenos), expires=next_year)
        response.set_cookie('divstyles', quote_plus(divstyles), expires=next_year)

        return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
