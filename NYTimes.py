import json
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
        url = "http://api.nytimes.com/svc/search/v1/article?format=json&query="+query+ \
              "&begin_date="+startDate+"&end_date="+endDate+"&rank=newest&api-key=" + api_key
    #    url = "http://api.nytimes.com/svc/mostpopular/v2/mostviewed/world/7.json?api-key=b2751dd1dd945ed4c4d17e39dbf78520:2:65203037"
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
        # write to a text file
        textname = query + "_nytimes.txt"
        output_file = open(textname,'w')
        output_file.write(str(listNews))
        output_file.close()
        
        return listNews
    
    except:
        print "Exception: ", sys.exc_info()[0]
        return news
    
# formats number to be used in date for the API call    
def get_str(number):
    if number < 10:
        return '0' + str(number)
    else:
        return str(number)


def main():
    countries = ['Mexico']
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
##    parse = [('http://www.nytimes.com/2011/11/06/world/europe/the-gridlock-where-debts-meet-politics-economic-memo.html', 'ECONOMIC MEMO; The Gridlock Where Debts Meet Politics - Economic Memo WASHINGTON &mdash; With Greece struggling to form a government that can force harsh austerity measures onto a weary public, Europe is in usual form, taking a couple of steps toward solving its fiscal crisis and then a couple of steps backward. Washington, meanwhile, is hoping that the latest deficit-reduction committee in Congress can succeed where'), ('http://www.nytimes.com/2011/11/06/sunday-review/the-secret-war-with-iran.html', 'NEWS ANALYSIS; The Secret War With Iran COMMUTING to work in Tehran is never easy, but it is particularly nerve-racking these days for the scientists of Shahid Beheshti University. It was a little less than a year ago when one of them, Majid Shahriari, and his wife were stuck in traffic at 7:40 a.m. and a motorcycle pulled up alongside the car. There was a faint &ldquo;click&rdquo; as a'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/in-an-iranian-prison-tortured-by-solitude.html', 'OPINION; In an Iranian Prison, Tortured by Solitude Oakland, Calif. AT 5:15 p.m. I found myself pacing compulsively back and forth across my 10-foot-by-14-foot cell in Iran&rsquo;s Evin prison, muttering reassurances to myself and kneading my nervous hands together into one fat fist. &ldquo;Don&rsquo;t worry,&rdquo; I told myself, &ldquo;this is probably your last day alone, they can&rsquo;t just'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/telling-americans-to-vote-or-else.html', 'OPINION; Telling Americans to Vote, or Else Washington JURY duty is mandatory; why not voting? The idea seems vaguely un-American. Maybe so, but it&rsquo;s neither unusual nor undemocratic. And it would ease the intense partisan polarization that weakens our capacity for self-government and public trust in our governing institutions. Thirty-one countries have some form of mandatory voting,'), ('http://www.nytimes.com/2011/11/06/nyregion/fighting-a-rare-disease-far-from-home-neediest-cases.html', 'THE NEEDIEST CASES; Thonn McMillan Fights Rare Disease Far From Home - Neediest Cases Numbers tell a stark story of Thonn McMillan&rsquo;s battle for survival against a rare disease that has wreaked havoc on his body. He is 17 years old and weighs 85 pounds. Two 15-gauge needles are inserted into a skin graft in his fragile left arm when he undergoes dialysis. He takes 28 pills and limits his drinking water to 12 ounces every day to'), ('http://travel.nytimes.com/2011/11/06/travel/flying-with-children-the-bad-and-the-worse.html', 'Flying With Children: the Bad and the Worse SURELY they could spare a little milk, right? But when John and Mary Rose Lin of Jersey City ran out of milk for their 18-month-old twins on a recent Continental flight from Newark to Maui , the flight attendant onboard refused to give them more. That particular beverage, the Lins recall being told, was for coffee, not children. &ldquo;I was not'), ('http://www.nytimes.com/2011/11/06/sports/bob-wielands-athletic-accomplishments-continue-to-inspire.html', 'Bob Wielands Athletic Accomplishments Continue to Inspire In Bob Wieland&rsquo;s world, obstacles create opportunities and conquests breed inspiration. Wieland was declared dead and taken away in a zipped-up body bag in 1969 after stepping on a mortar mine in Vietnam. But he awoke a half-hour later and now breathes life into battles against limitations with his speeches and ultradistance adventures that'), ('http://www.nytimes.com/2011/11/06/education/edlife/the-china-conundrum.html', 'The China Conundrum This article is a collaboration between The New York Times and The Chronicle of Higher Education , a daily source of news, opinion and commentary for professors, administrators and others interested in academe. Tom Bartlett is a senior writer at The Chronicle covering ideas and research; Karin Fischer is a senior reporter covering international'), ('http://www.nytimes.com/2011/11/06/world/middleeast/leaving-iraq-us-fears-new-surge-of-qaeda-terror.html', 'Leaving Iraq, U.S. Fears New Surge of Qaeda Terror BAGHDAD &mdash; As the United States prepares to withdraw its troops from Iraq by year&rsquo;s end, senior American and Iraqi officials are expressing growing concern that Al Qaeda &rsquo;s offshoot here, which just a few years ago waged a debilitating insurgency that plunged the country into a civil war, is poised for a deadly resurgence. Qaeda'), ('http://www.nytimes.com/2011/11/06/us/oklahoma-hit-by-earthquake-for-a-second-night-in-a-row.html', 'Oklahoma Hit by Earthquake for a Second Night in a Row For the second night in a row, an earthquake rattled Central Oklahoma late Saturday night, waking residents, breaking dishes and generally startling people more accustomed to natural disasters from above than from below their feet. The quake, which the United States Geological Survey said had a preliminary magnitude of 5.6, occurred about 10:53')]
##    parsedNews = NewsParser.newsParser(parse)
##    print parsedNews
     #   print "Query: %s\n%s\n\n\n%s" % (query, listNews, parsedNews)
        
if __name__ == '__main__':
    main()
