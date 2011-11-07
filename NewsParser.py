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
    print "here1"
    for link, text in news:
        print "here"
        text = text.lower()
        # get rid of all the punctuation
        for c in string.punctuation:
            text = text.replace(c, " ")
        text = text.split()
        # find all the keywords and the count
        newsDict, count = countWords(text)

        # prune articles that do not contain any keyword
        keys = newsDict.keys()
        print "keys", keys
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

##def main():
##    parse = [('http://www.nytimes.com/2011/11/06/world/europe/the-gridlock-where-debts-meet-politics-economic-memo.html', 'ECONOMIC MEMO; The Gridlock Where Debts Meet Politics - Economic Memo WASHINGTON &mdash; With Greece struggling to form a government that can force harsh austerity measures onto a weary public, Europe is in usual form, taking a couple of steps toward solving its fiscal crisis and then a couple of steps backward. Washington, meanwhile, is hoping that the latest deficit-reduction committee in Congress can succeed where'), ('http://www.nytimes.com/2011/11/06/sunday-review/the-secret-war-with-iran.html', 'NEWS ANALYSIS; The Secret War With Iran COMMUTING to work in Tehran is never easy, but it is particularly nerve-racking these days for the scientists of Shahid Beheshti University. It was a little less than a year ago when one of them, Majid Shahriari, and his wife were stuck in traffic at 7:40 a.m. and a motorcycle pulled up alongside the car. There was a faint &ldquo;click&rdquo; as a'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/in-an-iranian-prison-tortured-by-solitude.html', 'OPINION; In an Iranian Prison, Tortured by Solitude Oakland, Calif. AT 5:15 p.m. I found myself pacing compulsively back and forth across my 10-foot-by-14-foot cell in Iran&rsquo;s Evin prison, muttering reassurances to myself and kneading my nervous hands together into one fat fist. &ldquo;Don&rsquo;t worry,&rdquo; I told myself, &ldquo;this is probably your last day alone, they can&rsquo;t just'), ('http://www.nytimes.com/2011/11/06/opinion/sunday/telling-americans-to-vote-or-else.html', 'OPINION; Telling Americans to Vote, or Else Washington JURY duty is mandatory; why not voting? The idea seems vaguely un-American. Maybe so, but it&rsquo;s neither unusual nor undemocratic. And it would ease the intense partisan polarization that weakens our capacity for self-government and public trust in our governing institutions. Thirty-one countries have some form of mandatory voting,'), ('http://www.nytimes.com/2011/11/06/nyregion/fighting-a-rare-disease-far-from-home-neediest-cases.html', 'THE NEEDIEST CASES; Thonn McMillan Fights Rare Disease Far From Home - Neediest Cases Numbers tell a stark story of Thonn McMillan&rsquo;s battle for survival against a rare disease that has wreaked havoc on his body. He is 17 years old and weighs 85 pounds. Two 15-gauge needles are inserted into a skin graft in his fragile left arm when he undergoes dialysis. He takes 28 pills and limits his drinking water to 12 ounces every day to'), ('http://travel.nytimes.com/2011/11/06/travel/flying-with-children-the-bad-and-the-worse.html', 'Flying With Children: the Bad and the Worse SURELY they could spare a little milk, right? But when John and Mary Rose Lin of Jersey City ran out of milk for their 18-month-old twins on a recent Continental flight from Newark to Maui , the flight attendant onboard refused to give them more. That particular beverage, the Lins recall being told, was for coffee, not children. &ldquo;I was not'), ('http://www.nytimes.com/2011/11/06/sports/bob-wielands-athletic-accomplishments-continue-to-inspire.html', 'Bob Wielands Athletic Accomplishments Continue to Inspire In Bob Wieland&rsquo;s world, obstacles create opportunities and conquests breed inspiration. Wieland was declared dead and taken away in a zipped-up body bag in 1969 after stepping on a mortar mine in Vietnam. But he awoke a half-hour later and now breathes life into battles against limitations with his speeches and ultradistance adventures that'), ('http://www.nytimes.com/2011/11/06/education/edlife/the-china-conundrum.html', 'The China Conundrum This article is a collaboration between The New York Times and The Chronicle of Higher Education , a daily source of news, opinion and commentary for professors, administrators and others interested in academe. Tom Bartlett is a senior writer at The Chronicle covering ideas and research; Karin Fischer is a senior reporter covering international'), ('http://www.nytimes.com/2011/11/06/world/middleeast/leaving-iraq-us-fears-new-surge-of-qaeda-terror.html', 'Leaving Iraq, U.S. Fears New Surge of Qaeda Terror BAGHDAD &mdash; As the United States prepares to withdraw its troops from Iraq by year&rsquo;s end, senior American and Iraqi officials are expressing growing concern that Al Qaeda &rsquo;s offshoot here, which just a few years ago waged a debilitating insurgency that plunged the country into a civil war, is poised for a deadly resurgence. Qaeda'), ('http://www.nytimes.com/2011/11/06/us/oklahoma-hit-by-earthquake-for-a-second-night-in-a-row.html', 'Oklahoma Hit by Earthquake for a Second Night in a Row For the second night in a row, an earthquake rattled Central Oklahoma late Saturday night, waking residents, breaking dishes and generally startling people more accustomed to natural disasters from above than from below their feet. The quake, which the United States Geological Survey said had a preliminary magnitude of 5.6, occurred about 10:53')]
##    news = newsParser(parse)
##    print "Parsed: %s\n" % news
##        
##if __name__ == '__main__':
##    main()
