import string

keywords = ["tornado", "war", "quake", "earthquake"]  # for testing purposes

# newsParser( new )
# purpose: parse the news in text format and keeps a count for each distinct word
# preconditions: 
# parameters:
#       news - list of news: [("link", "text"), ("link2", "text")]
# returns:
#       newsList - list: [("link", dictionary with keywords, word count)]
def newsParser(news):
    newsList = []
    for link, text in news:
        text = text.lower()
        # get rid of all the punctuation
        for c in string.punctuation:
            text = text.replace(c, " ")
        text = text.split()
        # find all the keywords and the count
        newsDict, count = countWords(text)

        # prune articles that do not contain any keyword
        keys = newsDict.keys()
        if not (len(keys) == 1 and keys[0] == "other"):
            newsList.append((link, newsDict, count))
    return newsList

# countWords( text )
# purpose: find keywords in text and keep the count
# preconditions:
# parameters:
#       text - list of words
# returns:
#       tuple - (dictionary of keywords, total word count)
def countWords(text):
    d = {}
    d["other"] = 0                  # word is not in keywords
    totalCount = 0 
    for word in text:
        if word in d:               # word is a keyword and is recorded in d already
            d[word] += 1
        else:
            if word in keywords:    # word in keywords
                d[word] = 1
            else:                   # word is not in keywords
                d["other"] += 1
        totalCount += 1
    return (d, totalCount)

