from googlefinance import getQuotes
from datetime import datetime
from time import sleep,localtime
import threading
import os

"""
NOTES
- does not handle exceptions
- does not check if google finance works or not (if you get blacklisted then will recieve error 503)
- Need to think of how to implement linear regression slope
    - should probably save all quotes and handle it there
        - this means saving for each symbol it's own file
- should change printQuotes to logQuotes to save them. we do not need to print the prices, just results
NEED
-to add handle exceptions like http error 500 and 503
-need to check time for 9:30 cause not every stock is traded exactly at that time so the api gets the 4:00 data if no one has traded
"""
#important stuff before you start
root = os.getcwd() #change this if you want different folder

#useless stuff
price = 'LastTradePrice'
stockS = 'StockSymbol'
time = 'LastTradeTime'
exPrice = 'ExtHrsLastTradePrice'
exTime = 'ExtHrsLastTradeDateTimeLong'
allSymbols = 'GOOG,AAPL,NVDA,UCTT,NERV,DRYS'.split(',')
#index of the time hour, minute, and seconds
hour = 3
minu = 4
sec = 5


#list should be fixed sized so imagine them as circular list using % to get to the next one
#somewhere else should be saved the data to process longer time range
#****Going towards the idea of just loading data from a file and making calculations from there
price1Min = [0] * 60
price5Min = [[0]*60] * 5 #should take the array of the price1min to recycle
price1hour = [[0]*60] *10 #same as above
#...will figure out the rest once we make up the rules on figuring the slope of
#the linear regression wether to have all points(price per second) or have the average of
#the previous interval of time as it gets bigger, mainly becuase it will be a lot of data.
#the only reason to do it with a lot of data more accuracy but con is time to process it

"""
'''
equation of linear regression line
http://www.statisticshowto.com/how-to-find-a-linear-regression-equation/
y-intercept = ( sum(all y)*sum(all x^2) - sum(all x)* sum(all x *y) ) /
                ( N*sum(all x^2) - sum(all x)^2  )

slope = ( sum( all x*y)  - sum(all x) * sum(all y) ) /
            ( N*sum(all x^2) - sum(all x)^2 )

the idea of using linear regression in stocks is to state wether the trend is
bull, bear, or neutral. the trend can be have different time frames from 5
minutes, 10 minutes, 30 minutes, 1 hour, and so on.
to do this we just need the slope of the regression line. if it is positve then
it is a up trend, negative it is down trend, neutral can be defined by zero but
it is very unlikely so we have to redefine it with a range but the smaller the
better. 
'''

takes in
x = list
y = list
xSq = list
xy = list
N = integer (population)
debating to change this to just include a list of x and y or just a file containing this
also i think y doesnt matter since time is always upwards or constant or whatever
"""
def linearRegression(x, y, xSq, xy, N):
    sumX = sum(x)
    sumY = sum(y)
    sumXY = sum(xy)
    sumXSq = sum(xSq)
    return (sumXY - sumX * sumY) / (N * sumXSq - sumX*sumX)



#infinite loop for stock
def printQuotes(symbols=allSymbols):
    print threading.activeCount()
    print threading.enumerate()
    lTime = localtime() 
    print ("%s\t%s\t%s")% ("Symbol","Price","Last Time") #make it look nice for people who do not know what is happening *not necessary 
    for symbol in getQuotes(symbols):
        sPrice = symbol[price]
        sTime = symbol[time]
        #should write to log
        if((lTime[hour] > 15 or lTime[hour]*60+lTime[minu]< 570)
           and exPrice in symbol):
            #after market price and premarket use the same key
            #have to check if extra hour or pre market exist
                sPrice =  symbol[exPrice]
                sTime = symbol[exTime]
        print("%s\t%s\t%s")%(symbol[stockS],sPrice,sTime)
    print 'Current Time ', datetime.now()
    print
    t = threading.Timer(1,printQuotes)
    t.start()
    
def calculateSlope(time):
    return
    #time is in minutes
    #this should be another thread


#loading
def loading(s=10):
    print "initializing",
    for i in range(s-1):
        print".",
        sleep(1)
    print"."
    sleep(1)

#check this first to avoid errors
#these folders will be used to keep the data tidy
#NOTE: change the root for your computer
def checkFiles(symbols=allSymbols):
    print "current dir: ", root
    for s in symbols:
        if not os.path.exists(root+"/"+s):
            print "made folder for: ", s
            os.mkdir(root+"/"+s)
		
#checkFiles()
#loading(3)    
printQuotes()
