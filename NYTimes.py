import json
import time
import datetime
import sys
import urllib2
import unicodedata
import NewsParser

api_key = "8eea45b381642654c6ea186ead00f6c7:7:65075079"

# Crawls a NY Times 
def get_news(query):
    print "Getting News " 
    news = []
    today = datetime.date.today()
    twoDaysBefore = today - datetime.timedelta(2)
    startDate = str(twoDaysBefore.year) + get_str(twoDaysBefore.month) + get_str(twoDaysBefore.day )
    endDate = str(today.year) + get_str(today.month) + get_str(today.day)
    
    # gets news
    try:
        url = "http://api.nytimes.com/svc/search/v1/article?format=json&query="+query+ \
              "&begin_date="+startDate+"&end_date="+endDate+"&rank=newest&api-key=" + api_key
        #print url
        f = urllib2.urlopen(url)
        
        # Transfer the data to JSON format
        news = json.loads(f.read())
        f.close()
        return news["results"]
    
    except:
        print "Exception: ", sys.exc_info()[0]
        return news
    
def get_str(number):
    if number < 10:
        return '0' + str(number)
    else:
        return str(number)

def get_countries(filename):
    f = open(filename)
    countries = []
    for line in f:
        country = line.replace(' ','+')
        countries.append(country.split()[0])
    f.close()
    return countries

def main():
    countries = get_countries("countries.txt")
    for query in countries:
        listNews = []
        print query
        news = get_news(query)
        
        for doc in news:
            title = unicodedata.normalize('NFKD', doc["title"]).encode('ascii','ignore') 
            body = unicodedata.normalize('NFKD', doc["body"]).encode('ascii','ignore') 
            link = unicodedata.normalize('NFKD', doc["url"]).encode('ascii','ignore') 

            listNews.append((link, title + " " + body))
        output_file = open(query + ".txt", 'w')
        output_file.write("Query: %s\n%s" % (query, listNews))
        output_file.close()

        print "Query: %s\n%s\n\n\n%s" % (query, listNews, parsedNews)
        
if __name__ == '__main__':
    main()
