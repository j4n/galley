"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')
    #map.connect("/{filename:.*.?}", controller='view', action='index')
    # match all filenames for direct view
    map.connect("/{filename}", requirements={"filename": R".*?"}, controller='view', action='index')
    #map.connect("/{filename}", requirements={"filename": R".*\.[^/]{3,4}"}, controller='view', action='index')
    ## match all directories, with and without trailing slash - i.e. the rest
    #map.connect("/{path}", requirements={"path": R".*"}, controller='browse', action='index')
    ##map.connect("/{path:.*?}", controller='browse', action='index')

    return map
