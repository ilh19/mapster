
import os
import cgi
from scripts import twitter
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        is_result = True
        blank_country = True
        map_string = ''
        country_string = ''
        try:
            map_string = cgi.escape(self.request.get('map-radio'))
            country_string = cgi.escape(self.request.get('country'))
            
            if len(country_string) > 0:
                blank_country = False
        except:
            is_result = False
        
        map_url = ''
        tweets = []
        if not is_result:   
            map_url = self.get_map('All')
        else:
            map_url = self.get_map(map_string)
            if not blank_country:
                t = twitter.Twitter()
                tweets = t.return_frontpage_tweets(country_string)
        
        
        
        tweet_objs = []
        for tweet in tweets:
            tweet_objs.append(Tweet(tweet[0], tweet[1]))
        
        are_tweets = False
        if len(tweets) > 0:
            are_tweets = True
        
        template_values = {
            'map_url' : map_url,
            'tweets': tweet_objs,
            'are_tweets': are_tweets,
            'country': country_string,
            'blank_country': blank_country,
        }
        path = os.path.join(os.path.dirname(__file__), '../web/index.html')
        self.response.out.write(template.render(path, template_values))
        
    def get_map(self, result):
        if result == 'Nuclear':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301384+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Twitter':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301764+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Epidemic':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301395+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Politics':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301389+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Crime':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301765+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Other':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301499+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'NaturalDisasters':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301375+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        else:
            #all
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2301774+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'

class Tweet:
    def __init__(self, url, text):
        self.url = url
        self.text = text

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                     ('/index', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()