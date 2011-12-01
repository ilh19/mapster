#Mapster Project
#CSCE 470 - Fall 2011
#Lauren Dunn

from urllib2 import *
from django.utils import simplejson as json

#Bing API

class Bing_API:
    #no infomration needed to initialize this data type.
    #construct only contains key pieces of information such as the type of query (sources), AppID code for Mapster and base URL
    def __init__(self):
        self.app_id = 'FFCCED433B9A240742E0F537A82FE424288C67A9'
        self.sources = 'news'
        #don't remove blank string - this is for category-free search
        self.categories = ['', 'rt_Politics', 'rt_Health', 'rt_World']
                
        self.base_url = 'http://api.bing.net/json.aspx?AppId=%s&Version=2.2&Market=en-US&Query=%s&Sources=%s&JsonType=raw&News.SortBy=Relevance&Market=en-us'
        #location override parameter is only available for us states
        
        self.results = []
    
    #To get information from the Bing API, simply call the get news function on a Bing_API object.  
    #The only information you will need to pass it is the query.  The query can include spaces but should not include any other non-alphanumeric characters.
    #returns a list of tuples of the format (url, snippet text)
    #warning: there are sleeps in this function to prevent too many calls to the bing api (shouldn't be more than 7/sec).  It will take at least 1 second to return.
    def get_news(self, query):
        self.results = []
        if ' ' in query:
            query = query.replace(' ', '%20')
            
        for category in self.categories:
            time.sleep(.25)
            url = self.base_url % (self.app_id, query, self.sources)
            if len(category) > 0:
                url = url + '&News.Category=' + category
            
            try:
                f = urlopen(url)
                responses = json.loads(f.read())
                f.close()
                responses = responses[u'SearchResponse'][u'News'][u'Results']
                
                for response in responses:
                    result_url = response[u'Url'].encode('ascii', 'ignore')
                    if not self.url_is_in_results(result_url):
                        result_text = response[u'Snippet'].encode('ascii', 'ignore')
                        self.results.append((result_url, result_text))
            except:
               print "Exception in Bing API: ", sys.exc_info()[0]
               continue
        # write to a text file
        #textname = query + "_bing.txt"
        #output_file = open(textname,'w')
        #output_file.write(str(self.results))
        #output_file.close()
        return self.results
    
    #a simple boolean function to indicate if a url is in the current result set to prevent duplicate tuples.  This is for internal use only.
    def url_is_in_results(self, url):
        for pair in self.results:
            if url == pair[0]:
                return True
        return False
        
    """Response data type (case sensitive)
    SearchResponse
        Query
        Version
        News
            Total
            Results = list
                Title
                Url
                BreakingNews
                Snippet
                Source = such as Yahoo!
                Date
                NewsCollections
    """
        
#an example of how to use this class.
####def main(args):
####    
####    b = Bing_API()
####    while True:
####        country = raw_input('What country would you like news for? ')
####        for result in b.get_news(country):
####            print result[0]
####            print result[1]
####            print '-----'
####   
####
####if __name__ == '__main__':
####    import sys
####    main(sys.argv)
