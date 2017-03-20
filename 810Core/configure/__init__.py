#********************************Y.A.T********************************
'''
This module will be used for loading in data from 
configuration and/or data files(.yic).
'''
#********************************Y.A.T********************************
import re

#------------------------------------------------------------------------------
# Function for loading in tickers from tickers.yat
#------------------------------------------------------------------------------
def load_sector(input_sector):
    all_flag = False
    #open and load ticker file
    ticker_file = open('tickers.yat', 'r')
    file_data = ticker_file.readlines()
    ticker_file.close()
    read_tick = False
    ticker_list = []
    if(input_sector == 'ALL'):
       all_flag = True         
    for line in file_data:
        sector = re.search('###(.*?)###', line)
        if(sector and (sector.group(1) == input_sector) and (all_flag is False)):
            read_tick = not read_tick
        elif(all_flag and sector):
            read_tick = not read_tick        
        if(read_tick):
            ticker = re.search('\$(.*?)\!', line)
            if(ticker and (ticker.group(1) not in ticker_list)):     
                ticker_list.append(str(ticker.group(1)))            
    return(ticker_list)