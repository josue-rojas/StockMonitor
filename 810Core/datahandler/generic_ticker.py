#********************************Y.A.T********************************
'''
This class is a generic container for ticker data
'''
#********************************Y.A.T********************************

#------------------------------------------------------------------------------
# Generic ticker class
#------------------------------------------------------------------------------
class generic_ticker_data():

    def __init__(self):
        self.id = None
        self.symbol = None
        self.index = None
        self.price = None
        self.last_trade_time = None
        self.last_trade_date = None
        self.change = None
        self.change_percent = None
        self.aa_price = None

    def get_id(self):
        return (self.id)

    def set_id(self, id):
        self.id = id

    def get_symbol(self):
        return(self.symbol)

    def set_symbol(self, symbol):
        self.symbol = symbol

    def get_index(self):
        return(self.index)

    def set_index(self, index):
        self.index = index

    def get_price(self):
        return(self.price)

    def set_price(self, price):
        self.price = price

    def get_lst_trd_tm(self):
        return(self.last_trade_time)

    def set_lst_trd_tm(self, last_trade_time):
        self.last_trade_time = last_trade_time
        
    def get_lst_trd_date(self):
        return(self.last_trade_date)

    def set_lst_trd_date(self, last_trade_date):
        self.last_trade_date = last_trade_date
                
    def get_change(self):
        return(self.change)

    def set_change(self, change):
        self.change = change
                
    def get_prct_change(self):
        return(self.change_percent)

    def set_prct_change(self, change_percent):
        self.change_percent = change_percent
  
    def get_aa_price(self):
        return(self.aa_price)

    def set_aa_price(self, aa_price):
        self.aa_price = aa_price

