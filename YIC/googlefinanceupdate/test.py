from googlefinance import getQuotes
from googlefinance import getQuotesF
from googlefinance import getNews

import json

print json.dumps(getQuotesF('GOOG','ChangePercent'), indent=2)
#print json.dumps(getNews("GOOG"), indent=2)
