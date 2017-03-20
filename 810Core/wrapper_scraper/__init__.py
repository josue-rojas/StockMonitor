#********************************Y.A.T********************************
'''
This module will be used as an intermediate between different 
web scraping python modules, making this module a YIC proprietary 
'web scraping tool of web scraping tools'. Data verification between 
different sources will(at programmers discretion) also take place in
this module. If the percent difference between the same data captured 
from two different sources exceeds [X]% an exception or at the very 
least a warning must be thrown.(at programmers discretion)
'''
#********************************Y.A.T********************************
import yahoo_finance
import googlefinance
import ystockquote


#------------------------------------------------------------------------------
# Wrapper class for the googlefinance module
#------------------------------------------------------------------------------
class g_tick_data():

    def __init__(self, ticker):
        self.ticker = ticker
        self.tick_info = (googlefinance.getQuotes(ticker))

    def refresh(self):
        self.__init__(self.ticker) 
      
    def get_id(self, index=0):
        return (self.tick_info[index]["ID"])

    def get_tick(self, index=0):
        return(self.tick_info[index]["StockSymbol"])
        
    def get_index(self, index=0):
        return(self.tick_info[index]["Index"])
      
    def get_price(self, index=0):
        return((float)(self.tick_info[index]["LastTradePrice"]))
                
    def get_lst_trd_tm(self, index=0):
        return(self.tick_info[index]["LastTradeTime"])  
        
    def get_lst_trd_date(self, index=0):
        return(self.tick_info[index]["LastTradeDateTime"])
 
    def get_change(self, index=0):
        return((float)(self.tick_info[index]["Change"]))
        
    def get_prct_change(self, index=0):
        return((float)(self.tick_info[index]["ChangePercent"]))        
        
    def get_aa_price(self, index=0):
        return((float)(self.tick_info[index]["ExtHrsLastTradePrice"]))     
    
    def get_aa_lst_trd_tm(self, index=0):
        return(self.tick_info[index]["ExtHrsLastTradeDateTimeLong"])  

    def get_prev_close_price(self, index=0):
        return((float)(self.tick_info[index]["PreviousClosePrice"])) 
 

#------------------------------------------------------------------------------
# Wrapper class for the ystockquote module
#------------------------------------------------------------------------------ 
class yq_tick_data():

    def __init__(self, ticker):
        self.ticker = ticker

        # It is more efficient to get all the data at once then access what you need 
        # in the object, rather that call all the individual functions in the module
        self.tick_info = ystockquote.get_all(self.ticker)
        print(self.tick_info)

    def refresh(self):
        __init__(self.ticker)     
        
    def get_price(self):
        return ((float)(self.tick_info["price"]))

    def get_change(symbol):
        return (self.tick_info["change"])

    def get_volume(symbol):
        return (self.tick_info["volume"]) 
    
    def get_avg_daily_volume(symbol):
        return (self.tick_info["avg_daily_volume"])

    def get_stock_exchange(symbol):
        return (self.tick_info["stock_exchange"])

    def get_market_cap(symbol):
        return (self.tick_info["market_cap"])

    def get_book_value(symbol):
        return (self.tick_info["book_value"])

    def get_ebitda(symbol):
        return (self.tick_info["ebitda"])

    def get_dividend_per_share(symbol):
        return (self.tick_info["dividend_per_share"])

    def get_dividend_yield(symbol):
        return (self.tick_info["dividend_per_share"])

    def get_earnings_per_share(symbol):
        return (self.tick_info["dividend_per_share"])

    def get_52_week_high(symbol):
        return (self.tick_info["fifty_two_week_high"])

    def get_52_week_low(symbol):
        return (self.tick_info["fifty_two_week_low"])

    def get_50day_moving_avg(symbol):
        return (self.tick_info["fifty_day_moving_avg"])

    def get_200day_moving_avg(symbol):
        return (self.tick_info["two_hundred_day_moving_avg"])

    def get_price_earnings_ratio(symbol):
        return (self.tick_info["price_earnings_ratio"])

    def get_price_earnings_growth_ratio(symbol):
        return (self.tick_info["price_earnings_growth_ratio"])

    def get_price_sales_ratio(symbol):
        return (self.tick_info["price_sales_ratio"])

    def get_price_book_ratio(symbol):
        return (self.tick_info["price_book_ratio"])

    def get_short_ratio(symbol):
        return (self.tick_info["short_ratio"])
        
        
  
#------------------------------------------------------------------------------
# Class for comparing % difference between yahoo and google data
#------------------------------------------------------------------------------ 
        
       