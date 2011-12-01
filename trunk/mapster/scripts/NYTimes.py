import json
#Mapster Project
#CSCE 470 - Fall 2011
#Irma Lam 

import time
import datetime
import sys
import urllib2
import unicodedata

api_key = "8eea45b381642654c6ea186ead00f6c7:7:65075079"

# get_news( query )
# purpose: Crawls the NY Times news for a given query
# parameter:
#       query - location in string format
# returns:
#       listNews - list of news. Format: [(link, news)]
def get_news(query):
    news = []
    today = datetime.date.today()
    twoDaysBefore = today - datetime.timedelta(2)
    startDate = str(twoDaysBefore.year) + get_str(twoDaysBefore.month) + get_str(twoDaysBefore.day )
    endDate = str(today.year) + get_str(today.month) + get_str(today.day)

    # gets news
    try:
        url1 = "http://api.nytimes.com/svc/search/v1/article?format=json&query="+query+ \
              "&begin_date="+startDate+"&end_date="+endDate+"&rank=newest&api-key=" + api_key
        url = "http://api.nytimes.com/svc/search/v1/article?format=json&query=geo_facet%3A%5B"+query.upper()+ \
              "%5D&begin_date="+startDate+"&end_date="+endDate+"&rank=newest&api-key=" + api_key

        f = urllib2.urlopen(url)
        
        # Transfer the data to JSON format
        news = json.loads(f.read())
        f.close()
        news = news["results"]
        listNews = []
        # normalizes the text result
        for doc in news:
            title = unicodedata.normalize('NFKD', doc["title"]).encode('ascii','ignore') 
            body = unicodedata.normalize('NFKD', doc["body"]).encode('ascii','ignore') 
            link = unicodedata.normalize('NFKD', doc["url"]).encode('ascii','ignore') 

            listNews.append((link, title + " " + body))
        
        return listNews
    
    except:
        print "Exception in NYTimes API: ", sys.exc_info()[0]
        return news
    
# formats number to be used in date for the API call    
def get_str(number):
    if number < 10:
        return '0' + str(number)
    else:
        return str(number)

## Example
####def main():
####    countries = ['Japan']
####    for query in countries:
####        listNews = []
####        print query
####        news = get_news(query)
####
####        print news
####        
####if __name__ == '__main__':
####    main()
