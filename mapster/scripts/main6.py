#Mapster Project

#!/usr/bin/env python  
# import logging
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app
from scripts import updateTable

import logging

countries = ['United+Kingdom', 'Turkey', 'Germany', 'Malaysia', 'Mexico']
class CronMailer(webapp.RequestHandler):
    def get(self):
        logging.info("Get news: Started!")
        
        # updates table for maps
        updateTable.update(countries)
        
        #mail.send_mail(sender="irms19@gmail.com",
        #    to="irms19@gmail.com",
        #    subject="News retrieval complete!",
        #    body="Scores and tables have been updated 6 have been computed!")
        logging.info("Get news: Finished!")

application = webapp.WSGIApplication([('/cron6', CronMailer)],debug=True)
def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
