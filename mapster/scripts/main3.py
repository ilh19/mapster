#Mapster Project

#!/usr/bin/env python  
# import logging
from google.appengine.ext import webapp
from google.appengine.api import mail
from google.appengine.ext.webapp.util import run_wsgi_app
from scripts import updateTable

import logging

countries = ['United+Arab+Emirates', 'Colombia', 'Cuba', 'Dominican+Republic', 'Japan', 'North+Korea', 'South+Korea', 'Iran', 'Iraq', 'Afghanistan']
class CronMailer(webapp.RequestHandler):
    def get(self):
        logging.info("Get news: Started!")
        
        update = updateTable.update(countries)
        
        mail.send_mail(sender="irms19@gmail.com",
            to="irms19@gmail.com",
            subject="News retrieval complete!",
            body="Scores and tables have been updated 3 have been computed!")
        logging.info("Get news: Finished!")

application = webapp.WSGIApplication([('/cron3', CronMailer)],debug=True)
def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
