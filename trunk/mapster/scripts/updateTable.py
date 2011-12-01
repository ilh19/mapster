from clientlogin import ClientLogin
from sqlbuilder import SQL
import ftclient
from fileimporter import CSVImporter
import logging

import Countries


#print "START"
#logging.info("START")

#tableDict = {'crime/terrorism': 2301765, 'epidemics': 2301395, 'nuclear': 2301384, 'travel gov alert': 2301764, 'politics/religious': 2301389, 'total': 2301774, 'other': 2301499, 'natural disasters/weather': 2301375}
tableDict = {'crime/terrorism': 2301363, 'epidemics': 2301470, 'nuclear': 2301471, 'travel gov alert': 2301472, 'politics/religious': 2301364, 'total': 2301469, 'other': 2301365, 'natural disasters/weather': 2301362}
#dictionary = {}

def update(countryList):
    logging.info("START")
    dictionary = {}
    countries = Countries.Countries(countryList)
    dictionary = countries.countries
#f = open('results.txt','r')
#str1 = f.read()
#str1 = str1.replace("+"," ")
#dictionary = eval(str1)

#countries = Countries.Countries()
#dictionary = countries.countries

    token = ClientLogin().authorize("travelmapster@gmail.com", "lmgtfy12")
    ft_client = ftclient.ClientLoginFTClient(token)
      
    rid = []
    rid.append("ROWID")
    logging.info(str(dictionary))
    for i in dictionary:
        for a in tableDict:
            #print i
            #print a
            logging.info(i)
            logging.info(a)
            if not a in dictionary[i]:
                if not (ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1]) == '':
                   # print (ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1])
                    rowID = int(ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1])
                    if a == "total":
                        ft_client.query(SQL().update(tableDict[a], cols={'Score': 0}, row_id=rowID))
                    else:
                        ft_client.query(SQL().update(tableDict[a], cols={'Score': 0}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={"News1": ''}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={'News2': ''}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={'News3': ''}, row_id=rowID))
            else:
                if not (ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1]) == '':
                    print (ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1])
                    rowID = int(ft_client.query(SQL().select(tableDict[a], rid, "Country='%s'" %i)).split("\n")[1])
                    if a == "total":
                        ft_client.query(SQL().update(tableDict[a], cols={'Score': (dictionary[i])[a]}, row_id=rowID))
                    else:
                        links = ""
                        length = len(dictionary[i][a][1])
                        remaining = 3 - length
                        ll = []
                        for z in range(length):
                            ll.append(dictionary[i][a][1][z][0])
                        for z in range(remaining):
                            ll.append('')
                        logging.info(str(ll[0]))
                        logging.info(str(ll[1]))
                        logging.info(str(ll[2]))    
                        ft_client.query(SQL().update(tableDict[a], cols={'Score': (dictionary[i])[a][0]}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={"News1": ll[0]}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={"News2": ll[1]}, row_id=rowID))
                        ft_client.query(SQL().update(tableDict[a], cols={"News3": ll[2]}, row_id=rowID))
    logging.info("FINISHED UPDATING")
#print "FINISH"

####countries = ['Thailand', 'Brazil', 'Argentina', 'Austria', 'Russia', 'Morocco', 'South+Africa', 'Egypt', 'Saudi+Arabia', 'Syria']
####
####def main():
####    update(countries)
####
####if __name__ == '__main__':
####    main()
