import cgi
import os
import urllib
import string
from dummyhandlers import *
from postfunctions import *
from framehandlers import *
 
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

import twitter

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            self.redirect('/logged_in/index.html')
        
        DJTweets = twitter.getTweets("Dow%20Jones",5)
        NasdaqTweets = twitter.getTweets("Nasdaq",5)
        SP500Tweets = twitter.getTweets("S%26P%20500",5)
        
        template_values = {
            'loginurl': users.create_login_url('logged_in/index.html'),
            'DowJones': DJTweets,
            'Nasdaq': NasdaqTweets,
            'SP500': SP500Tweets,
            }
        path = os.path.join(os.path.dirname(__file__), 'default/index.html')
        self.response.out.write(template.render(path, template_values))


        

application = webapp.WSGIApplication(
                                     [('/', SendToIndex),
                                      ('/default/about.html', AboutPage),
                                      ('/default/contact.html', ContactPage),
                                      ('/default/index.html', MainPage),
                                      ('/default/signup.html', SignupPage),
                                      ('/default/why.html', WhyPage),
                                      ('/logged_in/portfolio.html', PortfolioPage),
                                      ('/logged_in/help.html', HelpPage),
                                      ('/logged_in/index.html', LoggedMain),
                                      ('/logged_in/settings.html', SettingsPage),
                                      ('/logged_in/quotes.html', QuotesPage),
                                      ('/logged_in/contact.html', LoggedContact),
                                      ('/logged_in/frames/frame_my_portfolio.html', MyPortfolioPage),
                                      ('/logged_in/frames/frame_buy_sell.html', BuySellPage),
                                      ('/logged_in/frames/frame_add_capital.html', AddCapitalPage),
                                      ('/logged_in/frames/frame_watch_list.html', WatchListPage),
                                      ('/logged_in/frames/frame_history.html', HistoryPage),
                                      ('/sign', GetQuote),
                                      ('/addwatch', AddWatch),
                                      ('/buysell', BuySell),
                                      ('/deletewatch', DeleteWatch),
                                      ('/removecapital', RemoveCapital),
                                      ('/addcapital', AddCapital)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
	