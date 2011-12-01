
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
            map_string = 'All'
            map_url = self.get_map(map_string)
        else:
            map_url = self.get_map(map_string)
            if not blank_country:
                t = twitter.Twitter()
                tweets = t.return_frontpage_tweets(country_string)
        
        if len(map_string) == 0:
            map_string = 'All'
        elif map_string == 'Crime':
            map_string = 'Crime & Terrorism'
        elif map_string == 'Politics':
            map_string = 'Politics & Religion'
        elif map_string == 'NaturalDisasters':
            map_string = 'Natural Disasters'
        
        
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
            'now_viewing': map_string
        }
        path = os.path.join(os.path.dirname(__file__), '../web/index.html')
        self.response.out.write(template.render(path, template_values))
        
    def get_map(self, result):
        if result == 'Nuclear':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310942+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Twitter':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2311029+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Epidemic':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310587+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Politics':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310592+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Crime':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310590+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'Other':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2311030+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        elif result == 'NaturalDisasters':
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310770+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'
        else:
            #all
            return '"http://www.google.com/fusiontables/embedviz?viz=MAP&q=select+col1%3E%3E1+from+2310593+&h=false&lat=-10&lng=0&z=2&t=1&l=col1%3E%3E1"'

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