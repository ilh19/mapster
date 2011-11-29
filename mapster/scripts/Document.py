import re

keywords = {"tornado": 0.5, "earthquake": 0.7, "quake": 0.7, "civil war": 0.5, "travelalert": 0.9, "emergency": 0.9, "travelwarning": 0.9} #testing purposes

# Creates a Document object that finds and keeps the frequency 
# of keywords in that document
class Document:
    # parameters:
    #   link - string with url of article
    #   news - string of title and body
    #   frequencies - dictionary containing all the frequencies in all the documents
    #   keywords - dictionary with keywords and scores 
    def __init__(self, link, news, frequencies, keywords):    
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


def main(args):
    link = "link1"
    news = "tornado tornado travelwarning"
    news2 = 'travelwarning civil emergency war war tornado quake ECONOMIC MEMO; The Gridlock Where Debts Meet Politics - Economic Memo WASHINGTON &mdash; With Greece struggling to form a government that can force harsh austerity measures onto a weary public, Europe is in usual form, taking a couple of steps toward solving its fiscal crisis and then a couple of steps backward. Washington, meanwhile, is hoping that the latest deficit-reduction committee in Congress can succeed where tornado war quake'
    frequencies = {}
    doc = Document(link, news, frequencies, keywords)
    print "score: ", doc.scores, "frequencies: ", frequencies
    
   
if __name__ == '__main__':
    import sys
    main(sys.argv)    
