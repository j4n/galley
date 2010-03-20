import Image
from StringIO import StringIO
from glob import glob
import os
import cgi

base_template = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<style>
body {
  font-family: "Lucida Grande", Verdana, "Bitstream Vera Sans", "Lucida Sans Unicode", sans-serif;
  background-color: gray;
  }
#directories {
  background-color: white;
  margin: 10px;
  padding: 5px;
  border: 1px solid black;
  }
#pictures {
  background-color: white;
  margin:10px;
  padding: 5px;
  border: 1px solid black;
  }
a.directory {
  margin: 5px;
  }
img {
  margin: 5px;
  }
</style>
<title>Real Basic Gallery</title>
</head>
<body>
<h1>Real Basic Gallery</h1>
%s
</body>
</html>
"""

class fsPicture(object):
    def __init__(self, root, template=base_template):
        self.template = template
        self.root = root

    def split_path_from_item(self, item):
        """removes the root directory from the path.  This lets us use the result as a
        web path."""
        return "/" + item.replace(self.root, '')

    def directory_listing(self, directory, path):
        """returns html for a directory listing"""
        files = ""
        directories = ""
        for item in glob(directory + "/*"):
            web_path = self.split_path_from_item(item)
            if os.path.isdir(item):
                directories += """<div class="directory"><a href="%s" class="directory">%s</a></div>""" % (web_path, web_path)
            elif os.path.isfile(item) and item.lower().endswith('.jpg'):
                files += """<div class="image">
                <img src="%s?thumbnail=200"><br/><a href="%s">%s</a></div>""" % (web_path, web_path, web_path)
        html = ""
        if directories:
            html += """<h2>Directories</h2><div id="directories">%s</div>""" % directories
        if files:
            html +=  """<h2>Pictures</h2><div id="pictures">%s</div>""" % files
        return html

    def picture(self, image, path):
        """returns raw binary image.  If query string of "thumbnail" is passed to the app
        the image is resized to a maximum of the argument.  For instance:
        /some_image.jpg?thumbnail=100"""
        i = Image.open(image)
        if self.query_string:
            try:
                size = cgi.parse_qs(self.query_string)
                size = size['thumbnail'][0]
                i.thumbnail((int(size), int(size)))
            except:
                pass
        s = StringIO()
        i.save(s, 'JPEG')
        return s.getvalue()

    def find_object(self, path):
        """finds the directory or picture referenced, returns the response and the mimetype"""
        item = os.path.join(self.root, *path.split('/'))
        if os.path.isdir(item):
            return ([self.template % self.directory_listing(item, path),], 'text/html')
        elif os.path.isfile(item) and item.lower().endswith('.jpg'):
            return ([self.picture(item, path),], 'image/jpeg')
        else:
            return ([self.template % 'not found'], 'text/html')

    def __call__(self, environ, start_response):
        """the entry point to the application"""
        self.query_string = environ.get('QUERY_STRING', False)
        response, mimetype = self.find_object(environ['PATH_INFO'])
        start_response('200 OK', [('content-type',mimetype)])
        return response
        
if __name__ == '__main__':
    from paste import httpserver, session
    import sys
    HERE = os.path.abspath(os.path.dirname(__file__))
    if len(sys.argv) > 1:
        picture_base = sys.argv[1]
    else:
        picture_base = os.path.join(HERE, '..', 'test_base/')
    print "serving from %s" % picture_base
    app = fsPicture(picture_base)
    #httpserver.serve(app, host='127.0.0.1', port='8080')
    httpserver.serve(app, host='0.0.0.0', port='8080')
