#!/usr/bin/env python
# Basic on-the-fly gallery
# based on the wsgi-example from Chris McAvoy
# http://code.google.com/p/mcavoy-public-works/source/browse/trunk/wsgi_gallery/fsPictures/fspictures/fspictures.py

# Todos:
# * figure out how to make the whitebox nice
# * align next-up-prev
# * design: film-like
# * prefetch
# * css: opera-bug: leftmost hover-label does not hover away
# * improve scaling quality
# * exiv-infos
# * next-buttons-positions-bug
# * pagination?
# * slide-show-fullscreen-mode
# * caching

import Image
from StringIO import StringIO
from glob import glob
import os
import cgi

base_template = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
  <style>
body {
  font-family: "Lucida Grande", Verdana, "Bitstream Vera Sans", "Lucida Sans Unicode", sans-serif;
  background-color: gray;
  }
.whitebox {
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
  margin-left: auto;
  margin-right: auto;
}
.imgteaser {
    margin: 0;
    overflow: hidden;
    float: left;
    position: relative;
    height: 235px
}
.imgteaser a {
    text-decoration: none;
    float: left;
}
.imgteaser a:hover {
    cursor: pointer;
}
.imgteaser a img {
    float: left;
    margin: 10px;
    border: none;
    padding: 10px;
    background: #fff;
    border: 1px solid #ddd;
}
.imgteaser a:hover .desc{
    display: block;
    font-size: 0.8em;
    padding: 10px 0;
    background: #111;
    filter:alpha(opacity=75);
    opacity:.75;
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=75)"; /*--IE 8 Transparency--*/
    color: #fff;
    position: absolute;
    top: 11px;
    left: 11px;
    padding: 10px;
    margin: 0;
/*    width: 200px;*/
    border-top: 1px solid #999;
}
.imgteaser a:hover .desc strong {
    display: block;
    margin-bottom: 5px;
    font-size:1.5em;
}
.imgteaser a .desc {    display: none; }
.imgteaser a:hover .more { visibility: hidden;}

/* spacer element to wrap container around all divs */
div.spacer {
  clear: both;
}

</style>
  <title>Gallery of: %s</title>
 </head>
 <body>
  <h1>Gallery of: %s</h1>
%s
 </body>
</html>
"""

view_template = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
 <head>
  <style>
body {
  font-family: "Lucida Grande", Verdana, "Bitstream Vera Sans", "Lucida Sans Unicode", sans-serif;
  background-color: gray;
  }
.whitebox {
  background-color: white;
  margin:10px;
  padding: 5px;
  border: 1px solid black;
  }
img {
  display:block;
  margin-left: auto;
  margin-right: auto;
  border: none;
}

.to-left { float: left; }
.to-right { float: right; }
.to-center {
  float: center;
  text-align: center;
}

.navigation {
  text-decoration: none;
  color: 0x000;
}


/* spacer element to wrap container around all divs */
div.spacer {
  clear: both;
}

</style>
  <title>Viewing: %s</title>
 </head>
 <body>
  <h1>%s</h1>
%s
 </body>
</html>
"""


class fsPicture(object):
    def __init__(self, root, template=base_template):
        self.template = template
        self.view_template = view_template
        self.root = root

    def split_path_from_item(self, item):
        """removes the root directory from the path.  This lets us use the result as a
        web path."""
        return "/" + item.replace(self.root, '')

    def directory_listing(self, directory, path):
        """returns html for a directory listing"""
        files = ""
        directories = ""
        if path != '/':
            directories += """<div class="directory"><a href=".." class="directory">..</a></div>"""
        for item in glob(directory + "/*"):
            web_path = self.split_path_from_item(item)
            if os.path.isdir(item):
                directories += """<div class="directory"><a href="%s" class="directory">%s</a></div>""" % (web_path, web_path)
            elif os.path.isfile(item) and item.lower().endswith('.jpg'):
                files += """
<!--   <div class="hovernote">-->
   <div class="imgteaser">
    <a href="%s?view=700">
     <img src="%s?resize=200" alt="%s"/>
     <span class="desc">%s</span>
    </a>
   </div>
""" % (web_path, web_path, web_path, os.path.basename(web_path))
        html = ""
        if directories:
            html += """<h2>Directories</h2><div class="whitebox">%s</div>""" % directories
        if files:
            html +=  """
<h2>Pictures</h2>
 <div class="whitebox">
  <div class="spacer">&nbsp;</div> <!-- needed to wrap outer div around all elements -->
  %s
  <div class="spacer">&nbsp;</div>
 </div>
<br/>""" % files
        return html

    def picture(self, image, path):
        """returns raw binary image.  If query string of "resize" is passed to the app
        the image is resized to a maximum of the argument.  For instance:
        /some_image.jpg?resize=100"""
        i = Image.open(image)
        if self.query_string:
            try:
                qs = cgi.parse_qs(self.query_string)
                size = qs['resize'][0]
                i.thumbnail((int(size), int(size)))
            except:
                pass
        s = StringIO()
        i.save(s, 'JPEG')
        return s.getvalue()

    def view(self, image, path, size):
        """Format output for a single-picture view"""
        html = ""
        html += """
   <div class='whitebox'>
    <a href="%s">
     <img src="%s?resize=%s" alt="%s"/>
    </a>
   </div>
""" % (path, path, size, path)

        other_images = glob(os.path.dirname(image) + "/*.[jJ][pP]*[gG]")
        current_index = other_images.index(image)

        if (current_index > 0):
            previous_index = current_index - 1
            html += """   <div class="to-left navigation"> <a href="%s?view=700">previous</a></div>""" % os.path.basename(other_images[previous_index])

            html += """   <div class="to-center navigation"> <a href="%s">up</a></div>""" % self.split_path_from_item(os.path.dirname(other_images[current_index]))

        if (current_index < ((len(other_images)) - 1)):
            next_index = current_index + 1
            html += """   <div class="to-right navigation"> <a href="%s?view=700">next</a></div>""" % os.path.basename(other_images[next_index])

        return html

    def find_object(self, path):
        """finds the directory or picture referenced, returns the response and the mimetype"""
        item = os.path.join(self.root, *path.split('/'))
        if os.path.isdir(item):
            return ([self.template % (path, path, self.directory_listing(item, path)),], 'text/html')
        elif os.path.isfile(item) and item.lower().endswith('.jpg'):
            if self.query_string:
#                try:
                    qs = cgi.parse_qs(self.query_string)
                    if qs and qs.has_key('view'):
                        return ([self.view_template % (os.path.basename(path), os.path.basename(path[1:]), self.view(item, path, qs['view'][0]))], 'text/html')
                    else:
                        return ([self.picture(item, path),], 'image/jpeg')
#                except:
#                    pass
            else:
                return ([self.picture(item, path),], 'image/jpeg')
        else:
            return ([self.template % (path, path, 'not found')], 'text/html')

    def __call__(self, environ, start_response):
        """the entry point to the application"""
        self.query_string = environ.get('QUERY_STRING', False)
        response, mimetype = self.find_object(environ['PATH_INFO'])
        start_response('200 OK', [('content-type',mimetype)])
        return response
        
if __name__ == '__main__':
    import sys
    HERE = os.path.abspath(os.path.dirname(__file__))
    if len(sys.argv) > 1:
        picture_base = sys.argv[1]
    else:
        picture_base = os.path.join(HERE, '.', 'test_base/')
    print "serving from %s" % picture_base
    app = fsPicture(picture_base)
#    from wsgiref.simple_server import make_server
#    make_server('', 8080, app).serve_forever()
    from paste import httpserver, session
    httpserver.serve(app, host='0.0.0.0', port='8080')
