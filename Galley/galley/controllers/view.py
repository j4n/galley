import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from galley.lib.base import BaseController, render

from pylons import config

import os

log = logging.getLogger(__name__)

class ViewController(BaseController):

	def index(self, filename):
		absolute_filename = os.path.join(config.app_conf['gallery_root'], *filename.split('/'))
		if os.path.exists(absolute_filename):
			if os.path.isdir(absolute_filename):
				return self.render_directory(absolute_filename)
			else:
				return self.render_file(absolute_filename)
			
		else:
			return "Error: file does not exist!"
	
	def render_directory(self, path):
		return "Directory: " + path
	
	def render_file(self, filename):
		return "Filename: " + filename
