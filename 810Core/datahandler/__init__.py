#********************************Y.A.T********************************
'''
This class handles and stores data for periodic processing. 
Ideally you'd want to get all the local data and then pass that on 
to a data processor. This class isn't meant to process the data it collects, but instead should call a processor 
'''
#********************************Y.A.T********************************
import wrapper_scraper
import generic_ticker
import threading
import Queue
import time

#------------------------------------------------------------------------------
# Data handler
#------------------------------------------------------------------------------
class datahandler():

    def __init__(self, callback):
        self.__data_pipeline = Queue.Queue()
        self.__local_storage = dict()
        if(callback):
            self.data_handler_callback(time.time())       

    def push(self, gen_tick_data):
        #only use to inject data from 
        self.__data_pipeline.put(gen_tick_data)
       
    def pop(self):
        #probably shouldn't ever be called, besides internally
        return self.__data_pipeline.get()    
            
    def data_converter(self, tickers, size):
        #interface(scraper) data to local data
        for index in range(size):
            gen_tick_data = generic_ticker.generic_ticker_data()
            gen_tick_data.set_symbol(tickers.get_tick(index))
            gen_tick_data.set_price(tickers.get_price(index))
            gen_tick_data.set_lst_trd_tm(tickers.get_lst_trd_tm(index))
            gen_tick_data.set_lst_trd_date(tickers.get_lst_trd_date(index))
            gen_tick_data.set_change(tickers.get_change(index))
            gen_tick_data.set_prct_change(tickers.get_prct_change(index))
            self.push(gen_tick_data)
            
    def store_local(self, gen_tick_data):
        if(gen_tick_data.get_symbol() in self.__local_storage):
            self.__local_storage[gen_tick_data.get_symbol()].append(gen_tick_data)
        
        else:
           #add if new          
           self.__local_storage[gen_tick_data.get_symbol()] = []

    def retrieve_local():
        return self.__local_storage    
                     
    def data_handler_callback(self, p_last_time, offset=30):
        last_time = p_last_time
        gen_tick_data = generic_ticker.generic_ticker_data()
        while(not self.__data_pipeline.empty()):
            gen_tick_data = self.pop()
            self.store_local(gen_tick_data)            
        last_time = last_time + offset 
        data_proc_thread = threading.Timer(last_time - time.time(), self.data_handler_callback, [last_time, offset])
        data_proc_thread.start()
    


