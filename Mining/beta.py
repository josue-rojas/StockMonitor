'''
About: this is a ticker scraper and data management for stocks
the point of this is to find possible stock picks that are bullish and cheap
cheap in the sense of price not valued.

Important Stuff:
- http://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas link for pandas select like from sql 

TODO OVERALL:
- add pre market and after martket? maybe but i do not think it is very important for long term trading
- ADD THREADING TO AVOID COLLISION OR MISSING INTERSECTION AND TO ADD DATA THAT
    INVOLVES EQUATIONS AT THE SAME TIME
- Remove or filter stocks with no trading done or closed stocks
    or add a column of last traded date and time
- in the future add ability to start scraping from with the assumption that stocks can change relation
'''
import csv
import pandas as pd
import re
import requests
from googlefinance import getQuotes
import time
from yahoo_finance import Share #has delay (i think)
import math
from scipy import stats

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
def mineNames(seed=['AAPL','NASDAQ'],start=True):
    if(2 == len(seed)):
        url = 'https://www.google.com/finance?q=' + seed[1] + '%3A' + seed[0]
        print url
    else:
        return 'SEED NOT RIGHT LENGTH'
    r = requests.get(url).text
    #look for ticker:" 
    relatedStocks = re.findall('(ticker:")([\w|\d|\.|-]*)(:)([\w|\d|-|\.]*)"',r)
    if not start:
        seen.append(seed[0]) #seen means visited it's page and scraped the stocks names
    queue.extend(
        [str(line[3]), str(line[1])] for line in relatedStocks
        if 'INDEX' not in str(line[1])
        and [str(line[3]), str(line[1])] not in queue
        and str(line[3]) not in seen
        )


'''
Gets:current price for ONE stock
ToDO:
- Test multiple stocks with one of them returning 400 error to see how that goes
    or moved checking all to another method to keep all other stocks updated
'''
def getPrice(name,attempt):
    try:
        if attempt == 0:
#            q = getQuotes(name)
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
            return [0,0] #should return none
    except:
        return get52HL(name,attempt+1)

'''
Gets: Slope for the list of days listed....
Note: should have list from greatest to lowest cause i do not want to waste on sorting
    plus if we get the 'a' which is smaller than 'c' the biggest then in theory 'c' data(omega) has 'a' data (only 1 request)
Info:https://www.quantshare.com/sa-426-6-ways-to-download-free-intraday-and-tick-data-for-the-us-stock-market
TODO:
- IMPORTANT max for minute interval is 15 days!!!! NEED TO FIND OTHER SOURCE EVEN IF THEY ARE CHOPPED
    - need to find other source for data for more days in linear regression
- looking into yahoo
-  https://finance.yahoo.com/quote/YHOO/history?period1=1337054400&period2=1494820800&interval=1d&filter=history&frequency=1d
- in the future add precheck if the stock is still trading before sending the request

'''
def getSlope(ticker,daysList=[1825,1095,365,183,92,31,7,3,1]):
    #https://www.google.com/finance/getprices?i=[PERIOD]&p=[DAYS]d&f=d,o,h,l,c,v&df=cpct&q=[TICKER]
    #in the url: d = date column, o = open, h = high, l = low, c = close, v = volume
    prices = requests.get('https://www.google.com/finance/getprices?i=60&p='
                 +str(daysList[0])
                 +'d&f=d,c&df=cpct&q='
                 +ticker).text.splitlines()
    print str(daysList[0])
    if len(prices) == 6: #no results
        return [None,None,None,None,None,None,None,None]
    slopes = []
    total = len(prices) - 7 #seven lines are info
    sumY = 0
    sumX = 0
    sumXY = 0
    sumXSq = 0
    end = False
    days = 0 #count the days
    for price in reversed(prices):
        actPrice = price.split(",")
        sumY+=eval(actPrice[1])
        sumX+=1
        sumXY+=(eval(actPrice[1])*sumX)
        sumXSq+=math.pow(sumX,2)
        if end: #Slope(b) = (N*Sum(XY) - (Sum(X))(Sum(Y))) / (N*Sum(X)sq - (sum(X))sq)
            top = ((sumX+1)*sumXY) - (sumX*sumY)
            bottom = ((sumX+1)*sumXSq) - (math.pow(sumX,2))
            slopes.append(top/bottom)
            end=False
        if '1' == (str(actPrice[0])): #should change this!??!?!
            #assume next one is the last of the day
            days+=1
            if days in daysList:
                end=True
            print actPrice
        if sumX == total:
            return slopes
        
'''
Returns: newEntry[name,index,price,low52,high52,
'''
def newEntry(st):
    HL52 = get52HL(st[0], 0)
    return [st[0],st[1],getPrice(st[0],0),HL52[0],HL52[1]]

def main():
    #initialize everything HERE
    mineNames()     #first stock init
    num = 0
    while len(queue) > 0:
        time.sleep(1)
        st = queue.pop(0)
        print "#" + str(num) + " " + str(newEntry(st)) #should write to csv here
        mineNames(st,start=False)
        num+=1

#main()

print getSlope('AAPL')
#print getPrice('LMT',0)
#mineNames(['SHA','900951'])
#print queue


    

