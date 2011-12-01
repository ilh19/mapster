#twitter.py
#Lauren Dunn
#Mapster, CSCE 470 Fall 2011

from urllib2 import *
import json
import unicodedata

#Twitter class to read from the US' TravelGov twitter account and UK's foreignoffice twitter account.  It searches all tweets by these two accounts for a given country.  Results are of the form [(travelgov url, string mash up of tweets'), (foreignoffice url, string mash up of tweets)]
class Twitter(object):
    #nothing is needed to initialize the object
    def __init__(self):
        self.user_ids = ['travelgov', 'foreignoffice']
        self.base_url = 'https://api.twitter.com/1/statuses/user_timeline.json?include_entities=true&include_rts=true&screen_name=%s&count=200&include_rts=false'
        self.link_base = 'http://www.twitter.com/%s'
        self.tweets = {}
        self.keywords = {"turmoil": 0.2, "riot": 0.2, "assassination": 0.4, "assassination attempt": 0.4, "no embassy": 0.6, "civil war": 0.7, "social unrest": 0.4, "armed conflict": 0.5, "violent demonstration": 0.3, "international tension": 0.2, "hurricane": 0.8, "cyclone": 0.8, "typhoon": 0.8, "tornado": 0.8, "tsunami": 0.8, "earthquake": 0.8 , "quake": 0.8, "wildfire": 0.6, "flood": 0.5, "avalanche": 0.8, "snow storm": 0.8, "blizzard": 0.8, "ice storm": 0.8, "dust storm":0.8, "sand storm": 0.8, "volcanic eruption": 0.8, "heatwave": 0.8, "nuclear meltdown": 0.8, "tropical storm": 0.8, "monsoon": 0.8, "drought": 0.8, "famine": 0.8, "oil spill":0.5, "oil leak": 0.5, "flu": 0.5, "influenza": 0.5, "west nile": 0.5, "swine flu": 0.5, "bomb": 0.7, "weapon": 0.8, "mass destruction": 0.8, "IED":0.7, "improvised explosive device": 0.7, "suicide":0.8, "roadside bomb": 0.8, "organized crime": 0.5, "chemical weapon": 0.7, "biological warfare": 0.6, "biological weapon": 0.6, "anthrax": 0.7, "poison": 0.7, "explosive": 0.7, "explosion": 0.7, "kidnapping": 0.5, "human traffic": 0.5, "sex traffic": 0.5, "nuclear bomb": 0.8, "nuclear explosion": 0.8, "nuclear disaster": 0.8, "environmental emergency": 0.9, "smog": 0.7, "pollution": 0.6, "high ozone level": 0.6,"#travelalert": 0.999, "#emergency": 0.999, "#travelwarning": 0.999}
    
    #Call this on a Twitter object. Calls the twitter api to retrieve the latest tweets
    def get_recent_posts(self):
        for id in self.user_ids:
            if self.remaining_hits():
                url = self.base_url % (id)
                
                try:
                    f = urlopen(url)
                except:
                    continue
                
                self.tweets[id] = json.loads(f.read())
               # print "Tweets", str(self.tweets)
        #return self.tweets


    #Enter a country. Results are of the form [(travelgov url, string mash up of tweets'), (foreignoffice url, string mash up of tweets)]. This is if there are tweets for the country.  It will return an empty list if there are no results.
    def get_tweets(self, country):
        country = country.replace('+', '%20')
        
        results = []
        for id in self.tweets:
            tweets = self.tweets[id]
            
            for tweet in tweets:
               #print "tweet", tweet
                total = []
                tweet_text = tweet[u'text'].encode('ascii', 'ignore')
                if country.lower() in tweet_text.lower():
                    total.append(tweet_text)
                
                text = ''.join(total)  
                link_url = self.link_base % id
                
                if len(text) > 0:
                    urls = []
                    #print "tweet", tweet
                    urls = tweet[u'entities'][u'urls']
                    if len(urls):
                        link = unicodedata.normalize('NFKD', urls[0][u'url']).encode('ascii','ignore') 
                        results.append((link, text))
                    else:
                        results.append((link_url,text))
                        
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
     
    def return_frontpage_tweets(self, country):
        self.get_recent_posts()
        tweets = self.get_tweets(country)
        
        return tweets
        
def main(args):
    t = Twitter()
    t.get_recent_posts()
    print t.get_tweets('thailand')
   # print t.get_tweets('saudi arabia')
    
   

if __name__ == '__main__':
    import sys
    main(sys.argv)
