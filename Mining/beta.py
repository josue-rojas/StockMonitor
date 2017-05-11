'''
About: this is a ticker scraper and data management for stocks
the point of this is to find possible stock picks that are bullish and cheap
cheap in the sense of price not valued.

Important Stuff:
- http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas link for pandas select like from sql 

TODO OVERALL:
- ***Change mining to a queue so that way we dont ignore missed stocks when crshed, this means writing it on file
    Also might not use threading since it is linear and not many things happening, unless....
- fix regex for mineNames to ignore the '.' in the beginning thus ignoring basic index funds
    but not the wieird ones like the chinese ones that are ust numbers just lik their stocks
- ADD THREADING TO AVOID COLLISION OR MISSING INTERSECTION AND TO ADD DATA THAT
    INVOLVES EQUATIONS AT THE SAME TIME
- scrape data using threading to compute the slopes concurrently
- Remove or filter stocks with no trading done or closed stocks
    or add a column of last traded date and time
- add a seen list, when the program starts scrape the csv file to fill in what it already has
- in the future add ability to start scraping from with the assumption that stocks can change rellation
'''
import csv
import pandas as pd
import re
import requests
from googlefinance import getQuotes
import time
from yahoo_finance import Share #has delay (i think)

#names and constants
#filename = 'ticks.csv'
filename = 'test.csv' #test file used for testing.....
numColumn = 14

#column names
name = 'name'
index = 'index'
price = 'price'
low52 = ' low52'
high52 = 'high52'
yrSlope5 = 'yrSlope5'
yrSlope3 = 'yrSlope3'
yrSlope1 = 'yrSlope1'
monSlope6 = 'monSlope6'
monSlope3 = 'monSlope3'
monSlope1 = 'monSlope1'
wkSlope1 = 'wkSlope1'
daySlope3 = 'daySlope3'
daySlope1 = 'daySlope1'
#these are tempory list for testing
tempNames=[]
tempCSV = []



'''
there should be 14 columns which include
all the things above 'column names in that order
TODO:
check for correct input on columns ie. if it takes int make sure its int
#might not be necceseary but just in case there is an eror in the code
'''
def add(list):
    if(numColumn == len(list)):
        newRow = ', '.join(list)
        with open(filename, 'a') as ticks:
            tickWrite = csv.writer(ticks)
            tickWrite.writerow(list)
        return 'ADDED: ' + newRow
    return 'NOTHING ADDED'

'''
Todo: return in a better format
this method returns a table sorted in whatever column you choose
'''
def getSortBy(sortBy=name):
    df = pd.read_csv(filename)
    df = df.sort_values(sortBy)
    return df


'''
this method scrapes names of google finance website.
for every stock there should be a related company which in theory similar to the
friends all being connected all companies should be somehow related to the point
you will see all of them.
the seed is the starting point
Gets (should be returned):[name, index, price, low52, high52, 
'''
def mineNames(seed=['NASDAQ','AAPL']):
    url = 'https://www.google.com/finance?q='
    if(2 == len(seed)):
        url = url + seed[0] + '%3A' + seed[1]
        print url
    else:
        return 'SEED NOT RIGHT LENGTH'
    r = requests.get(url).text
    #look for ticker:" 
    all = re.findall('(ticker:")([\w|\d|\.|-]*)(:)([\w|\d|\.|-]*)"',r)
    for a in all:
        sName = str(a[3])
        sIndex = str(a[1])
        if "." not in sName and sName not in tempNames:
                time.sleep(1)
                HL52 = get52HL(sName,0)
                newEntry = [sName,sIndex,getPrice(sName,0),HL52[0],HL52[1]]
                tempNames.append(sName)
                tempCSV.append(newEntry)
                print tempCSV
                mineNames([sIndex,sName])

'''
Gets:current price for ONE stock
ToDO:
- Test multiple stocks with one of them returning 400 error to see how that goes
    or moved checking all to another method to keep all other stocks updated
'''
def getPrice(name,attempt):
    try:
        if attempt == 0:
            q = getQuotes(name)
            for a in getQuotes(name):
                p = a['LastTradePrice']
                return eval(p)
        elif attempt == 1:
            return Share(name).get_price() #returns None if it doesnt exist
        else:
            return 0
    except:
        return getPrice(name,attempt+1)   #need to move this to a try and catch later
'''
Gets: current 52 week low and hugh
Todo:
    - should be able to update multiple stocks to keep stocks updated
'''
def get52HL(name,attempt):
    try:
        if attempt == 0:
            st = Share(name)
            return [st.get_year_low(), st.get_year_high()]
        else:
            return [0,0]
    except:
        return get52HL(name,attempt+1)
            
        
#print getPrice('LMT',0)
mineNames()
#mineNames(['SHA','900951'])


    

