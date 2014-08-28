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
from urllib import quote, unquote

from flask import Flask, make_response, render_template, request

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from tools import *


app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
        code = request.form.get('code', "print 'hello world!'")
        lexer = (
            request.form.get('lexer', '') or
            unquote(request.cookies.get('lexer', 'python')))
        lexers = [(l[1][0], l[0]) for l in get_all_lexers()]
        lexers = sorted(lexers, lambda a, b: cmp(a[1].lower(), b[1].lower()))
        style = (
            request.form.get('style', '') or
            unquote(request.cookies.get('style', 'colorful')))
        styles = sorted(get_all_styles(), key=str.lower)
        linenos = (
            request.form.get('linenos', '') or
            request.method == 'GET' and
            unquote(request.cookies.get('linenos', ''))) or ''
        divstyles = request.form.get(
            'divstyles', unquote(request.cookies.get('divstyles', '')))
        divstyles = divstyles or get_default_style()

        html = hilite_me(code, lexer, {}, style, linenos, divstyles)
        response = make_response(render_template('index.html', **locals()))

        next_year = datetime.datetime.now() + datetime.timedelta(days=365)
        response.set_cookie('lexer', quote(lexer), expires=next_year)
        response.set_cookie('style', quote(style), expires=next_year)
        response.set_cookie('linenos', quote(linenos), expires=next_year)
        response.set_cookie('divstyles', quote(divstyles), expires=next_year)

        return response

@app.route("/api", methods=['GET', 'POST'])
def api():
    code = request.values.get('code', '')
    if not code:
        response = make_response(render_template('api.txt'))
        response.headers["Content-Type"] = "text/plain"
        return response

    lexer = request.values.get('lexer', '')
    options = request.values.get('options', '')

    def convert(item):
        key, value = item
        if value == 'False':
            return key, False
        elif value == 'True':
            return key, True
        else:
            return key, value
    options = dict(convert(option.split('=')) for option in options.split(',') if option)

    style = request.values.get('style', '')
    linenos = request.values.get('linenos', '')
    divstyles = request.form.get('divstyles', get_default_style())

    html = hilite_me(code, lexer, options, style, linenos, divstyles)
    response = make_response(html)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
