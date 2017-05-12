'''
About: this is a ticker scraper and data management for stocks
the point of this is to find possible stock picks that are bullish and cheap
cheap in the sense of price not valued.

Important Stuff:
- http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas link for pandas select like from sql 

TODO OVERALL:
- ***Change mining to a queue so that way we dont ignore missed stocks when crshed, this means writing it on file
    Also might not use threading since it is linear and not many things happening, unless....
    - queue still using stack so we need to fix the crashing of to many stacks just restart the stacks
        since we already should be saving it.
- test after and pre market
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

seen=[] #all stocks that have been seen meaning pass through its URL
tempCSV = []
queue = []



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
To be used for initial start
Note: will clear previous queue
TODO: should be a csv rather than a regular txt, need to save index and stock name so [[name,index]] list
'''
def initQueue(clear=False):
    if clear == False:
        queue = [line.rstrip('\n') for line in open('SavedStateQueue')]

def initSeen(clear=False):
    if clear == False:
        return #read the csv and get the name column
'''
Todo: return in a better format
this method returns a table sorted in whatever column you choose
'''
def getSortBy(sortBy=name):
    df = pd.read_csv(filename)
    df = df.sort_values(sortBy)
    return df


'''
this method scrapes names of google finance website. adds to the queue to what should be searched
for every stock there should be a related company which in theory similar to the
friends all being connected all companies should be somehow related to the point
you will see all of them.
the seed is the starting point
'''
def mineNames(seed=['AAPL','NASDAQ']):
    if(2 == len(seed)):
        url = 'https://www.google.com/finance?q=' + seed[1] + '%3A' + seed[0]
        print url
    else:
        return 'SEED NOT RIGHT LENGTH'
    r = requests.get(url).text
    #look for ticker:" 
    relatedStocks = re.findall('(ticker:")([\w|\d|\.|-]*)(:)([\w|\d|-|.]*)"',r)
    queue.extend([str(line[3]), str(line[1])] for line in relatedStocks
                 if 'INDEX' not in str(line[1])
                 and str(line[3]) not in seen
                 and [str(line[3]), str(line[1])] not in queue)
    seen.append(seed[1]) #seen means visited it's page and scraped the stocks names
##    print queue
##    print 
##    #renewed
##    while len(queue) > 0:
##        st = queue.pop(0)
##        time.sleep(1)
##        HL52 = get52HL(st[0], 0)
##        newEntry = [st[0],st[1],getPrice(st[0],0),HL52[0],HL52[1]]
##        tempNames.append(st[0])
##        tempCSV.append(newEntry)
##        print tempCSV
##        mineNames([st[1],st[0]])

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

'''
Returns: newEntry[name,index,price,low52,high52,
'''
def newEntry(st):
    HL52 = get52HL(st[0], 0)
    return [st[0],st[1],getPrice(st[0],0),HL52[0],HL52[1]]

def main():
    #initialize everything HERE
    mineNames()     #first stock init
    while len(queue) > 0:
        time.sleep(1)
        st = queue.pop(0)
        mineNames(st)
        print newEntry(st) #should write to csv here

main()
    
#print getPrice('LMT',0)
#mineNames(['SHA','900951'])
#print queue


    

