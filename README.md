templeton, a minimal web framework
==================================

Templeton is a script, daemon, module, and support files intended for rapid
development of web applications.


Templeton apps
--------------

Templeton apps are essentially web.py apps with various enhancements and a
(highly) suggested structure.  They are managed by the templeton app server,
templetond.

The main goal of templeton is to streamline the process of developing and
deploying web apps.  While developing, templeton provides a simple development
server and a module to handle a lot of the underlying mechanics of modern web
apps, such as decoding URL search/query strings and serving simple Python
objects as JSON.  When the app is ready to deploy, the templeton app server
manages the app process and creates appropriate web-server config files.

Pursuant to this goal, templeton preserves the _relative_ URL path in
development and deployment.  The development server run at the root directory
of localhost on a given port.  When deployed, the app is configured to have the
same structure but live in a subpath, alongside other applications and content.

Templeton favours highly dynamic web sites based on the Single-Page Application
pattern.  To this end, static files are served at the base of the application's
path, and dynamic content is (by default) served under api/.  It is expected
that index.html would be a static file that, with the help of JavaScript, would
load dynamic content asynchronously.  At the same time, this dynamic data is
available at a known place to external applications.

(There are plans to remove this restriction so that templeton apps can also
follow a template-based pattern, with static content consisting mainly of
images, CSS, and JS.)

Templeton also packages up some common support web files, such as the jQuery
library.  The development server makes these available under /templeton.  For
deployment, the templeton command 'install' will copy the templeton/ directory
to the root of a web server's html dir, again, so the apps can link to these
files at a known location valid in both development and deployment modes.

For deployment, templeton currently supports nginx with spawn-fastcgi.


The templeton script
--------------------

The templeton script is the user's point of contact with the whole templeton
system.

Usage:

    templeton install <www-data-dir>

Copies support files (JS, CSS) into a "templeton" directory in www-data-dir.
The latter should be the root of the web site that will serve templeton
apps, since the template HTML file loads JS and CSS from /templeton.

    templeton init <appname>

Creates a new templeton project in a directory called appname, relative to
the current working directory.  If virtualenv is available, a virtualenv is
installed to the new directory, and the template files are installed to
appname/src/appname/.  If virtualenv is not available, the templates are
copied directly into appname/.

  You should be able to serve up your default app by doing

    # virtualenv available
    source <appname>/bin/activate
    cd <appname>/src/<appname>/server
    python server.py [port]  # [port] defaults to 8080

  or

    # no virtualenv
    cd <appname>/server
    python server.py [port]  # [port] defaults to 8080

Go to http://localhost:8080/ to see the result.  The next steps you'll want
to do is edit handlers.py and put in your server-side
business logic, and edit and create the files in ../html/ to build up
your client-side logic.


The rest of the commands interface with the templeton app server:

    templeton register

Registers the app in the current working directory with the app server.  This
also creates a web-server config file, for deployment.  Note that you
(probably) have to reload or restart your web server in order to pick up this
config.

    templeton unregister

Removes this app from the care of the app server.

    templeton disable

Tells the app server not to start this app automatically.

    templeton enable

Tells the app server to start this app automatically, if it was previously
disabled.

    templeton start

Starts the FastCGI process for dynamic content.

    templeton stop

Stops the FastCGI process.

    templeton list

Lists all templeton apps, with their status.


The templeton module
--------------------

The templeton module has two main functions:

* set up middleware to separate static pages from dynamic calls.
* provide helpers for common tasks, such as handling specific request types.


### middleware ###

The middleware module provides the patch_middleware() function to patch
web.py's development server to serve the app with the standard templeton
structure.  The server.py template includes the necessary call.


### handlers ###

templeton is geared toward client-rich, REST-based web applications.  These
typically involve a large amount of JSON.  templeton provides decorators to
simplify handler code.

* @json_response is a decorator function that expects the decorated function to
  return a JSON-serializable object, which it uses to construct a proper
  web.py response.

* @png_response expects the decorated function to return a PIL object, which it
  serves as a PNG image.

Both decoraters also redirect any URLs that don't end in a slash to one that
does, to enforce some consistency.  Thus if you access api/foo, it will
redirect to api/foo/.  Your handler URLs should reflect this.


The handlers module also provides helper functions.

load_urls() takes a web.py URL-handler sequence, i.e. (path, class_name,
path, class_name, ...), and prepends the REST API path, '/api', to each
given path.  The default server.py (created by the 'init' script command) uses
this function to load urls from handlers.py.

get_request_parms() parses the current request's search string and body as JSON
and returns the results as (args, body).

A trivial example of a JSON handler that echoes back any search-string args:

    import templeton

    urls = (
        '/test/?', 'JsonTest'
    )
    
    class JsonTest(object):
    
        @templeton.handlers.json_response
        def GET(self):
            args, body = templeton.handlers.get_request_parms()
            return args

With the development server running on port 8080,

    $ curl 'http://localhost:8080/api/test/?cat=meow&dog=bark&cat=purr'
    {"dog": ["bark"], "cat": ["meow", "purr"]}
