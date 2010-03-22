import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from galley.lib.base import BaseController, render

from pylons import config

import os, Image, mimetypes
from StringIO import StringIO

log = logging.getLogger(__name__)

class ViewController(BaseController):

	def index(self, filename):
		absolute_filename = os.path.join(config['gallery_root'], *filename.split('/'))
		if os.path.exists(absolute_filename):
			if os.path.isdir(absolute_filename):
				return self.render_directory(absolute_filename)
			else:
				return self.render_file(absolute_filename)
			
		else:
			return "Error: file '" + absolute_filename + "' does not exist!"

	def render_directory(self, path):
		return "Directory: " + path

	def render_file(self, filename):
		size = 700
		return render('/image.mako', extra_vars={'name': size})
		#return "Filename: " + filename

	def render_raw_file(self, filename):
		return self.render_image(filename)

	def render_resized_file(self, filename, resize=0):
		return self.render_image(filename, resize)

	def render_image(self, filename, resize=0):
		absolute_filename = os.path.join(config['gallery_root'], *filename.split('/'))
		response.content_type = self.get_mimetype(absolute_filename)
		image = Image.open(absolute_filename)
		if resize:
			image.thumbnail((int(resize), int(resize), Image.ANTIALIAS))
		image_string = StringIO()
		image.save(image_string, 'JPEG', quality=95)
		
		#response.content_type = 'image/jpeg'
		return (image_string.getvalue())

	def get_mimetype(self, filename):
		type, encoding = mimetypes.guess_type(filename)
		# We'll ignore encoding, even though we shouldn't really
		return type or 'application/octet-stream'