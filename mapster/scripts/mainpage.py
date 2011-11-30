
import os
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        is_result = True
        result_string = 'fff'
        """try:
            result_string = cgi.escape(self.request.get('map-radio'))
        except:
            is_result = False
        
        map_url = ''
        if not is_result:
            map_url = self.get_map('All')
        else:
            map_url = self.get_map(result_string)
            
        path = os.path.split(__file__)
        path = os.path.split(path[0])
        path = os.path.join(path[0], 'web/style.css')
        
        template_values = {
            'map_url' : map_url,
        }"""
        path = os.path.join(os.path.dirname(__file__), '../web/index.html')
        self.response.out.write(template.render(path, {}))
        
    def get_map(self, result):
        if result == 'Nuclear':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301384+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'Twitter':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301764+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'Epidemic':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301395+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'Politics':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301389+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'Crime':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301765+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'Other':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301499+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        elif result == 'NaturalDisasters':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301375+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        else:
            #all
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301774+&h=false&lat=0&lng=0&z=3&t=1&l=col1%3E%3E1"'
        

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/index', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()