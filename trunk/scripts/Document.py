keywords = {"tornado": 3, "war":2, "quake":4, "earthquake":4}  # for testing purposes

class Document:
    #
    #
    # parameter:
    #   link - string with url of article
    #   news - list of words
    #   frequencies - 
    def __init__(self, link, news, frequencies):    #title, body):
        self.link = link
        self.scores = self.countWords(news, frequencies)        # dictionary containing scores for each keyword found: keyword: score
                                                                # ( number of ocurrences * weight ) * doc frequency
      #  print self.scores

    # countWords( text )
    # purpose: find keywords in text and keep the count
    # preconditions:
    # parameters:
    #       text - list of words
    # returns:
    #       tuple - (dictionary of keywords, total word count)
    def countWords(self, text, frequencies):
        d = {}
        for word in text:
            if word in d:                 # word is a keyword and add the weight of that word
                d[word] += keywords[word]
            else:
                if word in keywords:                # word in keywords
                    d[word] = keywords[word]
                    if word in frequencies:         # frequency added the first time the keyword is found
                        frequencies[word] += 1
                    else:
                        frequencies[word] = 1
    
        return d
