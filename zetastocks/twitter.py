import urllib
from google.appengine.api import urlfetch

#Tweet class stores relavent information for our application in a class
class Tweet:
#Tweet constuctor. Takes a name, text (the tweet itself), id (of the tweet, not the user) and date.  All arguments should be strings.
    def __init__(self, img, n, t, i, d):        
        self.image = img
        self.name = n
        self.text = t
        self.id = i
        self.date = d
        self.link = "http://www.twitter.com/" + self.name + "/statuses/" + self.id
    
    #prints a Tweet (very basic)
    def display(self):
        print self.image
        print self.text
        print "posted by " + self.name + " at " + self.date
        print self.link
    
#getTweets gets the "size" most recent tweets about the stock "symbol" given. Symbol should be a string and size should be a integer an no larger than 15.  getTweets returns a list of Tweet objects   
def getTweets(symbol, size):
    #get information
    if len(symbol) <= 2:# check for single character stock
        symbol = symbol + "%20stock"
    if not ((symbol == "S%26P%20500") or (symbol == "Nasdaq") or (symbol == "Dow%20Jones")): #fix to allow searches on US markets, and not treat them like stocks.
        symbol = "%24" + symbol
    
    size = min(size, 15) #max of 15 tweets returned
    
    try:
        url = urllib.urlopen("http://search.twitter.com/search.json?q=%s" %(symbol))
        rawFile = url.read()
    except urlfetch.DownloadError:  # Catch timeout errors
        return []
    try:
        tweets = [] #intialize the container of tweets outside the loop
        
        failedSearch = rawFile.find("[]",0, len(rawFile)-1)
        if failedSearch != -1:
            return tweet
        
    
        #remove header/tralier data
        remWrapper = rawFile.split('[')
        remWrapper = remWrapper[1].split(']')
        dataList = remWrapper[0].split('},{')
        dataList[0] = dataList[0].lstrip('{')
        dataList[len(dataList)-1] = dataList[len(dataList)-1].rstrip('}')


        i = 0
        #iterate through all tweets returned
        for data in dataList:
            if i >= size: #only get so many tweets
                break;
            try:
                fields = data.split("\",\"")
                
                #Get user image url
                imgSplit = fields[0].split("\":\"")
                img = imgSplit[1]
                
                #Get date of tweet
                dateSplit = fields[1].split("\":\"")
                dateSplit = dateSplit[1].split("+")
                date = dateSplit[0]
                
                #get name of twitter user
                nameSplit = fields[2].split("\":\"")
                name = nameSplit[1]
                
                #get tweet text
                metadata = fields[3].split(",\"")
                metadata = metadata[2].split("ext\":\"")
                text = metadata[1]
                
                #get tweet id
                idSplit = fields[4].split(",\"")
                idSplit = idSplit[0].split(":")
                id = idSplit[1]

                newTweet = Tweet(img, name, text, id, date)
                tweets.append(newTweet)
            except IndexError:
                i = i - 1;
            i = i + 1
        #end dataList for-loop

        
    except IndexError:
        return tweets

    
    return tweets
#end getTweets


###################
#scrpting (examples)
###################

#Sample of how to use Tweet class
#x = Tweet("zetastocks","Buy Buy Buy!!","23455783","5:45 Today")
#x.display()

#Sample of how to use getTweets function
#y = getTweets("aapl", 5)
# -OR- 
#z = getTweets("Nasdaq",5)
#for ys in y:
#    ys.display()

    