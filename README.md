# hilite.me

[hilite.me](http://hilite.me/) is a small webapp that converts your code
snippets into pretty-printed HTML format, easily embeddable into blog posts and
websites.

## Development

To set up development environment you need to install nginx and virtualenv, then run:

    % virtualenv env
    % source env/bin/activate
    % pip install -r requirements.txt

Edit your main `nginx.conf`:

    http {
        ...
        include /path/to/hilite.me/nginx-dev.conf;
    }

Update the project location in `hilite.me/nginx-dev.conf` and restart nginx.

Add this line to your `/etc/hosts`:

    127.0.0.1  hilite.dev

Type `make run` and go to <http://hilite.dev/>. If static files don't load make
sure nginx has rx permissions for the `hilite.me/static` directory.
