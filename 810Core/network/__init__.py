#********************************YIC********************************
'''
This module will be used to verify connections to external servers.
'''
#********************************YIC********************************
import socket
from urllib2 import urlopen
from urllib2 import URLError
from urllib2 import HTTPError


#------------------------------------------------------------------------------
#Function for checking the connection to one external site
#    Pass in the website address and the timeout, default is 1 second
#    Return 1 if connection is established 0 otherwise
#------------------------------------------------------------------------------
def check_connection(net_address, timeout=1): #default of 1 second is more then enough
    try :
        socket.setdefaulttimeout(timeout) #timeout in seconds
        response = urlopen(net_address)
    except URLError, e:
        print('Connection to ' + ((str)(net_address)) + ' FAILED')
        print('Reason: ' + str(e.reason))
        return(0)
    except HTTPError, e:
        print('Connection to ' + ((str)(net_address)) + ' FAILED')
        print('Reason: ' + str(e.code))
        return(0)
    except Exception:
        print('Connection to ' + ((str)(net_address)) + ' FAILED')
        print('Reason: UNKNOWN ERROR')
        return(0)
    else :
        print('Connection to ' + ((str)(net_address)) + ' ACHIEVED')
        return(1)

        
#------------------------------------------------------------------------------
#Function for checking the connection to array of external site
#    Pass in the website address and the timeout, NO default timeouts
#    Return array of results: ['1 or 0'(pass or fail)]
#------------------------------------------------------------------------------
def check_connections(web_list):
    results = []
    for site in web_list:
        passfail = 1
        socket.setdefaulttimeout((float)(site[1])) #timeout in seconds
        try :
            response = urlopen(site[0])
        except URLError, e:
            passfail = 0
            print('Connection to ' + ((str)(site[0])) + ' FAILED')
            print('Reason: ' + str(e.reason))
        except HTTPError, e:
            passfail = 0
            print('Connection to ' + ((str)(site[0])) + ' FAILED')
            print('Reason: ' + str(e.code))
        except Exception:
            passfail = 0
            print('Connection to ' + ((str)(site[0])) + ' FAILED')
            print('Reason: UNKNOWN ERROR')
        else :
            print('Connection to ' + ((str)(site[0])) + ' ACHIEVED')
        results.append(passfail)
    return results

    
#------------------------------------------------------------------------------
#TODO: Add another iteration to read in websites from a file
#------------------------------------------------------------------------------ 
    

'''    
#Example usage:       
check_connection('http://google.com/', 1)
#Array format: ['website', 'timeout']
#A timeout of 1-2 second(s) is probably the best amount 
website_array = [\
['http://yic.com/', '1'], ['http://google.com/', '.8'], ['http://yahoo.com/', '.01'],\
['http://youtube.com/', '1'], ['http://bloomberg.com/', '1'] , ['http://pornhub.com/', '.001'],\
['http://reddit.com/', '2'] , ['http://stocktwits.com/', '3'], ['http://stackoverflow.com/', '5']] 
test_array = check_connections(website_array)
print(test_array)
'''