#Mapster Project
#CSCE 470 - Fall 2011
#Clarissa Soon

import urllib
import time
import urllib2
from urllib2 import *
import json
from xml.dom import minidom
import unicodedata


def get_news(inp):
    url = "http://api.usatoday.com/open/articles?search="+inp+\
          "&encoding=json&days=3&api_key=fh5kwbgjbxfp46q4p5fqqh5x "
    #url = "http://api.usatoday.com/open/articles?search=%s&encoding=json&days=3&api_key=fh5kwbgjbxfp46q4p5fqqh5x " %(inp2)
    l = []
    try:
        f = urllib2.urlopen(url)
        data = json.loads(f.read())
        f.close()
             
        for i in data["stories"]:
            a = (unicodedata.normalize('NFKD', i["link"]).encode('ascii','ignore'),\
                 unicodedata.normalize('NFKD', i["title"]).encode('ascii','ignore')+\
                 " "+unicodedata.normalize('NFKD', i["description"]).encode('ascii','ignore'))
            l.append(a)
    except:
        print "Exception in USAToday API: ", sys.exc_info()[0]

    #textname = inp.strip('\n\r') + "_usatoday.txt"
    #output_file = open(textname,'w')
    #output_file.write(str(l))
    #output_file.close()
    
    return l


def main():
    get_news("China")

if __name__ == '__main__':
    main()
