#twitter.py
#Lauren Dunn
#Mapster, CSCE 470 Fall 2011

from urllib2 import *
import json

#Twitter class to read from the US' TravelGov twitter account and UK's foreignoffice twitter account.  It searches all tweets by these two accounts for a given country.  Results are of the form [(travelgov url, string mash up of tweets'), (foreignoffice url, string mash up of tweets)]
class Twitter(object):
    #nothing is needed to initialize the object
    def __init__(self):
        self.user_ids = ['travelgov', 'foreignoffice']
        self.base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=%s&count=200&include_rts=false'
        self.link_base = 'http://www.twitter.com/%s'
    
    #Call this on a Twitter object. Enter a country.   Results are of the form [(travelgov url, string mash up of tweets'), (foreignoffice url, string mash up of tweets)]. This is if there are tweets for the country.  It will return an empty list if there are no results.
    def get_recent_posts(self, country):
        country = country.replace(' ', '%20')
    
        results = []
        for id in self.user_ids:
            if self.remaining_hits():
                url = self.base_url % (id)
                
                try:
                    f = urlopen(url)
                except:
                    continue
                
                tweets = json.loads(f.read()) 
                
                total = []
                
                for tweet in tweets:
                    tweet_text = tweet[u'text'].encode('ascii', 'ignore')
                    if country in tweet_text.lower():
                        total.append(tweet_text)
                
                text = ''.join(total)  
                link_url = self.link_base % id
                
                if len(text) > 0:
                    results.append((link_url, text))
                time.sleep(1)
        
        return results

    #checks for remaining hits
    #does not sleep until reset because that would harm the user experience
    #returns true if there are remaining hits
    #False otherwise (if there aren't or there are errors)
    def remaining_hits(self):
        query = "http://api.twitter.com/1/account/rate_limit_status.json"
        
        try:
            f = urlopen(query)
        except:
           return False            
        
        if f is not None:
            status = json.loads(f.read())  
            f.close()
            self.reset_time = status['reset_time']
            if status['remaining_hits'] > 0:
                return True
            else:
                return False
        return False
        f.close()
        
def main(args):
    t = Twitter()
    print t.get_recent_posts('turkey')
    
   

if __name__ == '__main__':
    import sys
    main(sys.argv)