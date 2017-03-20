#********************************Y.A.T********************************
'''
The gentle labourer shall no longer suffer!
Rise up and seize the means of production!
'''
#********************************Y.A.T********************************
import wrapper_scraper
import datahandler
import configure
import threading
import datetime
import network
import logging
import Queue
import time

#------------------------------------------------------------------------------
# 
#------------------------------------------------------------------------------

print('''
            @@@@@@@@@@@
                    __\_\__
         ___________|_____|___________
          \                         /
           \  O  O  O  O  O  O  O  /
^^^^^^^^^^^^\_____________________/^^^^^^^^^^^

Look at me, I\'m the Captain now
''')

print('What sector would you like to monitor?')
print('ex: \'TECH\', \'FINANCE\', \'BIOTECH\', \'ALL\'')

stocks = configure.load_sector(raw_input('>').upper())
print('\n\nMonitoring: ' + str(stocks).strip('[]') + '\n')    

logging.basicConfig(filename='logs/' + '.'\
.join((str(datetime.datetime.now())\
.split(':'))[:-1]) + '_LOG.txt')

#ticker data periodic callback
def ticker_periodic_callback(ticker, offset, p_last_time, pipeline):
    last_time = p_last_time
    try:
        ticker.refresh()
        pipeline.put(ticker)
    except Exception as e:
        logging.error(str(e) + ' - ' + str(datetime.datetime.now()))
    last_time = last_time + offset 
    ticker_thread = threading.Timer(last_time - time.time(), ticker_periodic_callback, [ticker, offset, last_time, pipeline])
    ticker_thread.start()
    
print('Checking connection to internet...')
google_conn = network.check_connection('http://google.com/')

if (google_conn):
    data_pipeline = Queue.Queue(10)
    print('Running...')
    tickers = wrapper_scraper.g_tick_data(stocks)
    ticker_periodic_callback(tickers, 2, time.time(), data_pipeline)
    data_handler = datahandler.datahandler(True)
    
    while(1):
        try:       
            data_handler.data_converter(data_pipeline.get(True, 10), len(stocks))
        except Queue.Empty:
            logging.warning('Pipeline is empty - ' + str(datetime.datetime.now())) 
        except Exception as e:
            logging.error(str(e) + ': - ' + str(datetime.datetime.now()))
            
            