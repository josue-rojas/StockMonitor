from googlefinance import getQuotes
from googlefinance import getNews

import json

#no filter
print json.dumps(getQuotes('CHY'), indent=2)
#print json.dumps(getNews("GOOG"), indent=2)
#filter
print json.dumps(getQuotes('GOOG','ChangePercent,Yield'), indent=2)
print json.dumps(getNews('GOOG','URL'), indent=2)

