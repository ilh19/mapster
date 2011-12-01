import re

keywords = {"turmoil": 0.2, "riot": 0.2, "assassination": 0.4, "assassination attempt": 0.4, "no embassy": 0.6, "civil war": 0.7, "social unrest": 0.4, "armed conflict": 0.5, "violent demonstration": 0.3, "international tension": 0.2, "hurricane": 0.8, "cyclone": 0.8, "typhoon": 0.8, "tornado": 0.8, "tsunami": 0.8, "earthquake": 0.8 , "quake": 0.8, "wildfire": 0.6, "flood": 0.5, "avalanche": 0.8, "snow storm": 0.8, "blizzard": 0.8, "ice storm": 0.8, "dust storm":0.8, "sand storm": 0.8, "volcanic eruption": 0.8, "heatwave": 0.8, "nuclear meltdown": 0.8, "tropical storm": 0.8, "monsoon": 0.8, "drought": 0.8, "famine": 0.8, "oil spill":0.5, "oil leak": 0.5, "flu": 0.5, "influenza": 0.5, "west nile": 0.5, "swine flu": 0.5, "bomb": 0.7, "weapon": 0.8, "mass destruction": 0.8, "IED":0.7, "improvised explosive device": 0.7, "suicide":0.8, "roadside bomb": 0.8, "organized crime": 0.5, "chemical weapon": 0.7, "biological warfare": 0.6, "biological weapon": 0.6, "anthrax": 0.7, "poison": 0.7, "explosive": 0.7, "explosion": 0.7, "kidnapping": 0.5, "human traffic": 0.5, "sex traffic": 0.5, "nuclear bomb": 0.8, "nuclear explosion": 0.8, "nuclear disaster": 0.8, "environmental emergency": 0.9, "smog": 0.7, "pollution": 0.6, "high ozone level": 0.6,"#travelalert": 0.999, "#emergency": 0.999, "#travelwarning": 0.999}

# Creates a Document object that finds and keeps the frequency 
# of keywords in that document
class Document:
    # parameters:
    #   link - string with url of article
    #   news - string of title and body
    #   frequencies - dictionary containing all the frequencies in all the documents
    #   keywords - dictionary with keywords and scores 
    def __init__(self, link, news, frequencies):    
        self.keywords = keywords
        self.link = link
        self.total_words = 0
        self.scores = self.countWords(news, frequencies)        # dictionary containing scores for each keyword found: keyword: score
                                                                # ( number of ocurrences * weight ) * doc frequency
      #  print self.scores

    # countWords( text )
    # purpose: find keywords in text and keep the count
    # preconditions:
    # parameters:
    #       text - string to analyze
    #       frequencies - dictionary for the entire query {"keyword": frequency}
    # returns:
    #       tuple - (dictionary of keywords, total word count)
    def countWords(self, text, frequencies):
        d = {}
        self.total_words = len(text.split())
        for keyword in self.keywords:                           # finds all the keywords present in the text
            match = re.compile(keyword)
            allMatches = match.findall(text)
            if len(allMatches):                                 # keyword in text
                freq = len(allMatches)                          # frequency of keyword in text
                d[keyword] = freq * self.keywords[keyword]      # calculates the weight * freq of keyword
                if keyword in frequencies:                      # times the keyword appears a the document
                    frequencies[keyword] += 1
                else:
                    frequencies[keyword] = 1

        return d

## Example
####def main(args):
####    link = "link1"
####    news = "tornado tornado travelwarning"
####    news2 = 'travelwarning civil emergency war war tornado quake ECONOMIC MEMO; The Gridlock Where Debts Meet Politics - Economic Memo WASHINGTON &mdash; With Greece struggling to form a government that can force harsh austerity measures onto a weary public, Europe is in usual form, taking a couple of steps toward solving its fiscal crisis and then a couple of steps backward. Washington, meanwhile, is hoping that the latest deficit-reduction committee in Congress can succeed where tornado war quake'
####    frequencies = {}
####    doc = Document(link, news, frequencies, keywords)
####    print "score: ", doc.scores, "frequencies: ", frequencies
####    
####   
####if __name__ == '__main__':
####    import sys
####    main(sys.argv)    
