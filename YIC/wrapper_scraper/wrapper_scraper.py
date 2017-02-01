#********************************YIC********************************
'''
This module will be use as an intermediate between different 
web scraping python modules, making this module a YIC proprietary 
web scraping tool of web scraping tools. Data verification between 
different sources will(at programmer discretion) also take place in
this module. If the percent difference between the same data captured 
from two different sources exceeds [X]% an exception or at the very 
least a warning must be thrown.(at programmer discretion)
'''
#********************************YIC********************************
import yahoo_finance
import googlefinance
import json
import ystockquote

'''
We either need our own personal stock ticker database or we must pull it from somewhere 
'''

#------------------------------------------------------------------------------
# Wrapper class for google finance stock data
#------------------------------------------------------------------------------
class ticker_data():

    def __init__(self, ticker):
        self.ticker = ticker
        self.tick_info = json.loads(googlefinance.request(self.ticker))[0]
        
    def get_tick(self):
        return(self.tick_info["t"])
        
    def get_price(self):
        return(self.tick_info["l"])
        
    def get_index(self):
        return(self.tick_info["e"])

    def get_aa_price(self):
        return(self.tick_info["el_fix"])     
    
    def get_lst_trd_tm(self):
        return(self.tick_info["ltt"])  

        
##ignore what is below, it's just for testing 
test1 = ystockquote
print(test1.get_all("DRYS")["volume"])

test0 = ticker_data(['DRYS'])    

print(test0.get_price())
print(test0.get_tick())
print(test0.get_aa_price())
print(test0.get_lst_trd_tm())
