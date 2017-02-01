import json
import sys
import demjson

"""
this is my updated version of googlefinance 0.7 api https://github.com/hongtaocai/googlefinance
i added 
- names for json news request i cannot join them with the others cause there is overlap on keys.
- filter to get specific things from keys 


Things to add
-------------
- make another method to get a desire amount of results for news. 
- maybe join the url method (it might make it unclear to people but i dont like seeing to many methods that do the same)
"""
try:
    from urllib.request import Request, urlopen
except ImportError:  # python 2
    from urllib2 import Request, urlopen

__author__ = 'Hongtao Cai'

googleFinanceKeyToFullName = {
    u'id'     : u'ID',
    u't'      : u'StockSymbol',
    u'e'      : u'Index',
    u'l'      : u'LastTradePrice',
    u'l_cur'  : u'LastTradeWithCurrency',
    u'ltt'    : u'LastTradeTime',
    u'lt_dts' : u'LastTradeDateTime',
    u'lt'     : u'LastTradeDateTimeLong',
    u'div'    : u'Dividend',
    u'yld'    : u'Yield',
    u's'      : u'LastTradeSize',
    u'c'      : u'Change',
    u'c'      : u'ChangePercent',
    u'el'     : u'ExtHrsLastTradePrice',
    u'el_cur' : u'ExtHrsLastTradeWithCurrency',
    u'elt'    : u'ExtHrsLastTradeDateTimeLong',
    u'ec'     : u'ExtHrsChange',
    u'ecp'    : u'ExtHrsChangePercent',
    u'pcls_fix': u'PreviousClosePrice'
}



googleFinanceNewsKeyToFullName = {
	u'usg' : u'USER?/Referal', #https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwiq9r-CoOvRAhWJbSYKHQAxBj4QFggaMAA&url=http%3A%2F%2Fnews.softpedia.com%2Fnews%2FHackers-Find-Method-to-Bypass-Google-Redirect-Notice-219150.shtml&usg=AFQjCNEjX_RU_3Kd_EJL0ZKOscCwb6DXog&sig2=rk7N7Ti3kNiuYa_Px8vK-g&bvm=bv.145822982,d.eWE
	u'd'   : u'DatePosted',
	u'tt'  : u'IDK',
	u'sp'  : u'Summary',
	u's'   : u'Source',
	u'u'   : u'URL',
	u't'   : u'Title',
	u'sru' : u'GoogleURL'
}

def buildUrl(symbols):
    symbol_list = ','.join([symbol for symbol in symbols])
    # a deprecated but still active & correct api
    return 'https://finance.google.com/finance/info?client=ig&q=' \
        + symbol_list

def buildNewsUrl(symbol, qs='&start=0&num=1'):
   return 'https://www.google.com/finance/company_news?output=json&q=' \
        + symbol + qs

def request(symbols):
    url = buildUrl(symbols)
    req = Request(url)
    resp = urlopen(req)
    # remove special symbols such as the pound symbol
    content = resp.read().decode('ascii', 'ignore').strip()
    content = content[3:]
    return content

def requestNews(symbol):
    url = buildNewsUrl(symbol)
    print "url: ", url
    req = Request(url)
    resp = urlopen(req)
    content = resp.read()

    content_json = demjson.decode(content)

    #print "total news: ", content_json['total_number_of_news']

    article_json = []
    news_json = content_json['clusters']
    for cluster in news_json:
        for article in cluster:
            if article == 'a':
                article_json.extend(cluster[article])

    return article_json

def replaceKeys(quotes, isNews=False):
    keys = googleFinanceKeyToFullName if not isNews else googleFinanceNewsKeyToFullName
    quotesWithReadableKey = []
    for q in quotes:
        qReadableKey = {}
        for k in keys:
            if k in q:
                qReadableKey[keys[k]] = q[k]
        quotesWithReadableKey.append(qReadableKey)
    return quotesWithReadableKey
    

#filters for keys you want
def keyFilter(data,key):
	key = key.split(',')
	useful = []
	all = data
	for q in all:
		filter = {}
		for k in key:
			if k in q:
				filter[k] = q[k]
		useful.append(filter)
	return useful
	

def getQuotes(symbols,key=None):
    '''
    get real-time quotes (index, last trade price, last trade time, etc) for stocks, using google api: http://finance.google.com/finance/info?client=ig&q=symbols

    Unlike python package 'yahoo-finance' (15 min delay), There is no delay for NYSE and NASDAQ stocks in 'googlefinance' package.

    example:
    quotes = getQuotes('AAPL')
    return:
    [{u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'129.09', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'129.09', u'Yield': u'1.46', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'0.47', u'StockSymbol': u'AAPL', u'ID': u'22144'}]

    quotes = getQuotes(['AAPL', 'GOOG'])
    return:
    [{u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'129.09', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'129.09', u'Yield': u'1.46', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'0.47', u'StockSymbol': u'AAPL', u'ID': u'22144'}, {u'Index': u'NASDAQ', u'LastTradeWithCurrency': u'571.34', u'LastTradeDateTime': u'2015-03-02T16:04:29Z', u'LastTradePrice': u'571.34', u'Yield': u'', u'LastTradeTime': u'4:04PM EST', u'LastTradeDateTimeLong': u'Mar 2, 4:04PM EST', u'Dividend': u'', u'StockSymbol': u'GOOG', u'ID': u'304466804484872'}]

    :param symbols: a single symbol or a list of stock symbols
    :return: real-time quotes list
    '''
    if type(symbols) == type('str'):
        symbols = [symbols]
    content = json.loads(request(symbols))
    returnInfo = replaceKeys(content)
    if key is not None: #change the return if there are any filter keys
    	returnInfo = keyFilter(returnInfo,key)
    	
    return returnInfo;

def getNews(symbol,keys=None):
	#return requestNews(symbol);
	returnInfo = replaceKeys(requestNews(symbol),True)
	if keys is not None:
		returnInfo = keyFilter(returnInfo,keys)
		
	return returnInfo;

if __name__ == '__main__':
    try:
        symbols = sys.argv[1]
    except:
        symbols = "GOOG,AAPL"

    symbols = symbols.split(',')

    print(json.dumps(getNews("GOOG"), indent=2))
    print(json.dumps(getQuotes(symbols), indent=2))        
