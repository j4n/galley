import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from galley.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HelloController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/hello.mako')
        # or, return a response
        #response.content_type = 'text/plain'
        return render('/hello.mako')

    def environ(self):
        result = '<html><body><h1>Environ</h1>'
        for key, value in request.environ.items():
            result += '%s: %r <br />'%(key, value)
        result += '</body></html>'
        return result
