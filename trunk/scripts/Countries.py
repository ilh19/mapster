#Mapster Project
#CSCE 470 - Fall 2011
#Irma Lam

import GeoLocation
import bing_api
import NYTimes
import twitter
import USAToday

filename = "countries.txt"

# Calls all the API for each country and calculates their scores per category calling GeoLocation class
class Countries:
    # parameters:
    # data members:
    #       countries - ["country": [("link", score)]
    def __init__(self):
        self.countries = self.call_apis()      

    # get_countries( )
    # purpose: to obtain the list of countries from a textfile
    # returns:
    #       countries - array with name of countries
    def get_countries(self):
        f = open(filename)
        countries = []
        for line in f:
            line.strip('\n\r')
            line = line.replace(' ','+')
            countries.append(line.split()[0])
        f.close()
        print "countries", countries
        return countries

    # call_apis( )
    # purpose: calls the different apis for each country and concatenate the news
    # returns:
    #       countriesDict - dictionary of countries and news
    def call_apis(self):
        countries = self.get_countries()
        countriesDict = {}
        for country in countries:
            bing_news = bing_api.Bing_API()             # creates the Bing API object
            twitter_tweets = twitter.Twitter()
            news = NYTimes.get_news(country)            # NYTimes 
            news.extend(USAToday.get_news(country))     # USAToday
            news.extend(bing_news.get_news(country))    # Bing API
            news.extend(twitter_tweets.get_recent_posts(country)) # Twitter API
            print "Country: %s " % country
            
            location = GeoLocation.GeoLocation(news)      # calculates the scores for each category
            countriesDict[country] = location.categories  # assigns those categories

        self.write_file(countriesDict)
        
        return countriesDict

    # write_file( dict )
    # purpose: to write the score dictionary of each country to a text file
    #   in the following form:
    #       country
    #       dictionary of scores by category
    #       Note: if score >0.1: not safe
    #                      <0.1 : safe
    def write_file(self, dict):
        # write to a text file
        textname = "results.txt"
        output_file = open(textname,'a')
        output_file.write(str(dict))
        for country in dict:
            cat = dict[country]
            output_file.write(country + '\n')
            for category in cat:
                output_file.write(category + ": " + str(cat[category]) + '\n')
            #output_file.write("\n\n")
        output_file.close()
    

def main():
    countries = Countries()
    c = countries.countries
    for country in c:
        cat = c[country]
        print "COUNTRY: ", country
        for category in cat:
            print category, ": ", cat[category]
            print"\n"
        print"\n\n"
        
if __name__ == '__main__':
    main()
