import urllib
import time
import urllib2
from urllib2 import *
import json
from xml.dom import minidom
import unicodedata


def get_news(inp):
    url = "http://api.usatoday.com/open/articles?search="+inp+\
          "&encoding=json&days=3&api_key=gc9xgxv22npsym9zk5mbv7r3"
    #url = "http://api.usatoday.com/open/articles?search=%s&encoding=json&days=3&api_key=gc9xgxv22npsym9zk5mbv7r3" %(inp2)
    f = urllib2.urlopen(url)
    data = json.loads(f.read())
    f.close()
    
    l = []
    for i in data["stories"]:
        a = (unicodedata.normalize('NFKD', i["link"]).encode('ascii','ignore'),\
             unicodedata.normalize('NFKD', i["title"]).encode('ascii','ignore')+\
             " "+unicodedata.normalize('NFKD', i["description"]).encode('ascii','ignore'))
        l.append(a)

    textname = inp.strip('\n\r') + "_usatoday.txt"
    output_file = open(textname,'w')
    output_file.write(str(l))
    output_file.close()
    
    return l


def main():
    usaToday("China")

if __name__ == '__main__':
    main()
