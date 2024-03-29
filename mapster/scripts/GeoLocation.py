#Mapster Project
#CSCE 470 - Fall 2011
#Irma Lam

import Document
import string

categoriesDict = {"politics/religious": ["turmoil", "riot", "assassination", "assassination attempt", "no embassy", "civil war", "social unrest", "armed conflict", "violent demonstration", "international tension"], "natural disasters/weather": ["hurricane", "cyclone", "typhoon", "tornado", "tsunami", "earthquake", "quake", "wildfire", "flood", "avalanche", "snow storm", "blizzard", "ice storm", "dust storm", "sand storm", "volcanic eruption", "heatwave", "nuclear meltdown", "tropical storm", "monsoon", "drought", "famine", "oil spill", "oil leak"], "epidemics": ["flu", "influenza", "west nile", "swine flu"], "crime/terrorism":["bomb", "weapon", "mass destruction", "IED", "improvised explosive device", "suicide", "roadside bomb", "organized crime", "chemical weapon", "biological warfare", "biological weapon", "anthrax", "poison", "explosive", "explosion", "kidnap", "human traffic", "sex traffic"], "nuclear": ["nuclear bomb", "nuclear disaster", "nuclear explosion"], "other": ["environmental emergency", "smog", "pollution", "high ozone level"], "travel gov alert": ["#travelalert", "#emergency", "#travelwarning"]}
twitter_alert = ["#travelalert", "#emergency", "#travelwarning"]

# Class that obtains all the news and tweets, calculates their safety score, and top links
class GeoLocation:
    # parameters:
    #       news - list of news: [("link", "text"), ("link2", "text")]  from the APIs
    # data members:
    #       listDocs - list of Document objects after parsing the text in news
    #       frequencies - dictionary containing keywords and the number of ocurrences across documents
    #       categories - dictionary of categories. category: (score, top 3 links)
    def __init__(self, news):
        self.frequencies = {}
        #self.keywords = self.read_file("keywords.txt")                  # dictionary: { "keyword": score in between 0 and 1 }
        self.categoriesDict = categoriesDict #self.read_file("categories.txt")          # dictionary: { "category": ["keywords"] }
        self.listDocs = self.newsParser(news)
        self.categories = self.findCategories()

    # newsParser( news )
    # purpose: parse the news in text format and keeps a count for each distinct word
    # preconditions: 
    # parameters:
    #       news - list of news: [("link", "text"), ("link2", "text")]
    # returns:
    #       newsList - dictionary with keywords and scores
    def newsParser(self, news):
        newsList = []
        for link, text in news:
            text = text.lower()
            
            # create a new Document object and find all the keywords
            document = Document.Document(link, text, self.frequencies)
            
            # prune articles that do not contain any keyword
            if(len(document.scores)):  
                newsList.append(document)

        for keyword in self.frequencies:
            for doc in newsList:
                #print "scores ", doc.scores
                if keyword in doc.scores: 
                  #  print "doc.scores[keyword] ", doc.scores[keyword]
                    if  keyword in twitter_alert:          # higher weighting if it's a tweet
                        self.frequencies[keyword] = len(newsList)- 0.5
                    if self.frequencies[keyword] > 2:      # appears in more than 2 news articles, has higher weight
                        doc.scores[keyword] *= float(self.frequencies[keyword]/ float(len(newsList)))
                    else:
                        doc.scores[keyword] /= float(3 * len(newsList))
                  #  print "keyword: ", keyword, "-score: ", doc.scores[keyword], "-number of articles: ", len(newsList), "\nfrequencies: ", self.frequencies
        return newsList

    # findCategories( )
    # purpose: find the score for each category      
    # returns:
    #       categories - dictionary of categories. category: (score, top 3 links)
    def findCategories(self):
        categories = {}
        for doc in self.listDocs:
            scores = doc.scores
            for word in scores:
                for cat in self.categoriesDict:
                    if word in self.categoriesDict[cat]:
                        if cat in categories:                       # category was created
                            score, link, total = categories[cat]    # score for the category; list of tuples: (link, score)
                            score += scores[word] 
                            categories[cat] = (score, self.__insertLink(link, doc.link, scores[word]), total + 1)  
                            
                        else:                               # creates the category
                            categories[cat] = (scores[word], [(doc.link, float("%.3f" % scores[word]))], 1)

        total_score = 0
        #print categories
        #normalizes the scores per category and calculates the total severity score
        for cat in categories:
            score, link, total = categories[cat]
            score /= float(total)
            total_score += score
            categories[cat] = (float("%.3f" % score), link)

        # average scores across categories
        if len(categories):
            categories["total"] = float("%.3f" % (total_score / float(len(categories))))
            
        #print "categories", categories
        return categories

    # insertLink( link, wordLink, score )
    # purpose: determines if wordLink is in the top 3 links for that category
    # preconditions: 
    # parameters:
    #       link - list of tuples with top 3 links. [('link', socre)]
    #       wordLink - link for keyword
    #       score - score for that keyword
    # returns:
    #       link - updated list with top 3 links
    def __insertLink(self, link, wordLink, score):
        linkList = [l for l,s in link]
        if link in linkList:           # link is in list
            return link
        if len(link) < 3:               # link has less than 3 links
            link.append((wordLink, float("%.3f" % score)))
        else:                           # link has 3 links
            if score > link[2][1]:      # compares score with last link
                link.pop()
                link.append((wordLink, float("%.3f" % score)))
        
        link = sorted(link, key = lambda score: score[1], reverse = True)
        #print "link ", link
        return link

    # read_file( )
    # purpose: to read the dictionary from a text file
    # preconditions: 
    # returns:
    #       dictionary  - dictionary form of the text file
    def read_file(self, filename):
        f = open(filename)
        dictionary = {}
        line = ""
        for l in f:
            line = l.strip('\n')

        dictionary = eval(line)
         
        return dictionary

## Example       
##def main():
##    news_sample =[("link1", "tornado tornado #travelwarning something else"), ("link2", "tornado tornado blah blah blha"), ("link3", "hurricane #emergency blah blah blha")]
##    news = [('http://www.nytimes.com/2011/11/06/world/europe/the-gridlock-where-debts-meet-politics-economic-memo.html', 'war war tornado quake ECONOMIC MEMO; The Gridlock Where Debts Meet Politics - Economic Memo WASHINGTON &mdash; With Greece struggling to form a government that can force harsh austerity measures onto a weary public, Europe is in usual form, taking a couple of steps toward solving its fiscal crisis and then a couple of steps backward. Washington, meanwhile, is hoping that the latest deficit-reduction committee in Congress can succeed where tornado war quake'), ('http://www.nytimes.com/2011/11/06/sunday-review/the-secret-war-with-iran.html', 'NEWS ANALYSIS; tornado tornado war The Secret War With Iran COMMUTING to work in Tehran is never easy, but it is particularly nerve-racking these days for the scientists of Shahid Beheshti University. It was a little less than a year ago when one of them, Majid Shahriari, and his wife were stuck in traffic at 7:40 a.m. and a motorcycle pulled up alongside the car. There was a faint &ldquo;click&rdquo; as a'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/in-an-iranian-prison-tortured-by-solitude.html', 'OPINION; In an Iranian Prison, Tortured by Solitude Oakland, Calif. AT 5:15 p.m. I found myself pacing compulsively back and forth across my 10-foot-by-14-foot cell in Iran&rsquo;s Evin prison, muttering reassurances to myself and kneading my nervous hands together into one fat fist. &ldquo;Don&rsquo;t worry,&rdquo; I told myself, &ldquo;this is probably your last day alone, they can&rsquo;t just'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/telling-americans-to-vote-or-else.html', 'OPINION; Telling Americans to Vote, or Else Washington JURY duty is mandatory; why not voting? The idea seems vaguely un-American. Maybe so, but it&rsquo;s neither unusual nor undemocratic. And it would ease the intense partisan polarization that weakens our capacity for self-government and public trust in our governing institutions. Thirty-one countries have some form of mandatory voting,'), ('http://www.nytimes.com/2011/11/06/nyregion/fighting-a-rare-disease-far-from-home-neediest-cases.html', 'THE NEEDIEST CASES; Thonn McMillan Fights Rare Disease Far From Home - Neediest Cases Numbers tell a stark story of Thonn McMillan&rsquo;s battle for survival against a rare disease that has wreaked havoc on his body. He is 17 years old and weighs 85 pounds. Two 15-gauge needles are inserted into a skin graft in his fragile left arm when he undergoes dialysis. He takes 28 pills and limits his drinking water to 12 ounces every day to'), ('http://travel.nytimes.com/2011/11/06/travel/flying-with-children-the-bad-and-the-worse.html', 'Flying With Children: the Bad and the Worse SURELY they could spare a little milk, right? But when John and Mary Rose Lin of Jersey City ran out of milk for their 18-month-old twins on a recent Continental flight from Newark to Maui , the flight attendant onboard refused to give them more. That particular beverage, the Lins recall being told, was for coffee, not children. &ldquo;I was not'), ('http://www.nytimes.com/2011/11/06/sports/bob-wielands-athletic-accomplishments-continue-to-inspire.html', 'Bob Wielands Athletic Accomplishments Continue to Inspire In Bob Wieland&rsquo;s world, obstacles create opportunities and conquests breed inspiration. Wieland was declared dead and taken away in a zipped-up body bag in 1969 after stepping on a mortar mine in Vietnam. But he awoke a half-hour later and now breathes life into battles against limitations with his speeches and ultradistance adventures that'), ('http://www.nytimes.com/2011/11/06/education/edlife/the-china-conundrum.html', 'The China Conundrum This article is a collaboration between The New York Times and The Chronicle of Higher Education , a daily source of news, opinion and commentary for professors, administrators and others interested in academe. Tom Bartlett is a senior writer at The Chronicle covering ideas and research; Karin Fischer is a senior reporter covering international'), ('http://www.nytimes.com/2011/11/06/world/middleeast/leaving-iraq-us-fears-new-surge-of-qaeda-terror.html', 'Leaving Iraq, U.S. Fears New Surge of Qaeda Terror BAGHDAD &mdash; As the United States prepares to withdraw its troops from Iraq by year&rsquo;s end, senior American and Iraqi officials are expressing growing concern that Al Qaeda &rsquo;s offshoot here, which just a few years ago waged a debilitating insurgency that plunged the country into a civil war, is poised for a deadly resurgence. Qaeda'), ('http://www.nytimes.com/2011/11/06/us/oklahoma-hit-by-earthquake-for-a-second-night-in-a-row.html', 'Oklahoma Hit by Earthquake for a Second Night in a Row For the second night in a row, an earthquake rattled Central Oklahoma late Saturday night, waking residents, breaking dishes and generally startling people more accustomed to natural disasters from above than from below their feet. The quake, which the United States Geological Survey said had a preliminary magnitude of 5.6, occurred about 10:53')]
##    news_tweets = [('http://www.twitter.com/travelgov', 'travelalert #Turkey: U.S. citizens who may need assistance from #TurkeyQuake, contact Turkish Authorities or U.S. Consulate Adana: +90-322-346-6262.#Turkey: U.S. citizens should enroll in STEP program to obtain updated info on safety & security. http://t.co/drC2QuOf #TurkeyQuake#Turkey: U.S. citizens who need assistance, contact Turkish Authorities or U.S. Consulate Adana: +90-322-346-6262. #TurkeyQuake #Earthquake#Turkey: At this point, we have received no reports of U.S. citizens killed or injured in the #earthquake. cc: @USEmbassyTurkey #TurkeyQuake'), ('http://www.twitter.com/foreignoffice', 'RT @BritishMonarchy: The Queen and The Duke of Edinburgh have bidden farewell to the President of the Republic of Turkey and Mrs Gl #Tu ...RT @WilliamJHague: UK-Turkey relations stronger than ever. Vital partner in #foreignpolicy & our economic ties are increasingly importan ...RT @BritishMonarchy: The Queen has officially welcomed The President of the Republic of Turkey and Mrs Gl to the UK on Horseguards Para ...RT @BritishMonarchy: Gun salutes mark the start of the #Turkey State Visit: 41 guns in Green Park and 62 guns at the Tower of London @fo ...RT @WilliamJHague: State Visit by President Gl of Turkey begins today. First in 23 years. Welcome to Britain. @trpresidency @TC_DisisleriBritain and #Turkey: a new special relationship - Foreign Secretary @WilliamJHague writes in @TelegraphNews http://t.co/spQpdysx')]
##    location = GeoLocation(news_sample)
##    scores = [x.scores for x in location.listDocs]
##    print "Scores: %s \nfrequencies: %s" % (scores, location.frequencies)
##    print "Categories: ", location.categories
##
##    file = "results.txt"
##    results = location.read_file(file)
##
##    for country in results:
##        print country
##        r = results[country]
##        for cat in r:
##            print cat, r[cat]
##    
##        
##if __name__ == '__main__':
##    main()

