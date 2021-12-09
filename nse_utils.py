import requests
# from pprint import pprint
session = requests.session()

INDEX_LIST = ["NIFTY 50", "NIFTY NEXT 50"]
STOCK_LIST = ["SBIN"]

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

INDEX_URL = "https://www.nseindia.com/api/chart-databyindex?index=NIFTY%2050&indices=true&preopen=true"



# COOKIES
def getCookies():
    try:
        print("catching cookies...")
        BASE_URL = "https://www.nseindia.com/get-quotes"
        r = session.get(BASE_URL, headers=headers, timeout=5)
        cookies = dict(r.cookies)
        print("cookies received.")
# //////////////////////////
        print(cookies)
# //////////////////////////
        return cookies
    except requests.exceptions.Timeout:
        print("Timeout while accessing cookies")
        return None



# STOCK
def stock_quote(symbol):
    symbol = requests.utils.quote(symbol.upper())
    STOCK_URL = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"

    cookies = getCookies()
    if( not( cookies )): return None
    
    try:
        print(f"Getting quote for {symbol}")
        response = requests.get(STOCK_URL, headers=headers, cookies=cookies)
        quote = dict(response.json())
        print("SUCCESS")
        return quote
    except requests.exceptions.Timeout:
        print("Timeout while getting quote")
        return None



# INDEX
def index_quote(symbol):
    symbol_utf8_encoded = requests.utils.quote(symbol.upper())
    INDEX_URL = f"https://www.nseindia.com/api/chart-databyindex?index={symbol_utf8_encoded}&indices=true&preopen=true"
    try:
        print(f"Getting quote for {symbol}")
        response = requests.get(INDEX_URL, headers=headers, timeout=5)
        quote = dict(response.json())
        print("SUCCESS")
        return quote
    except requests.exceptions.Timeout:
         print("Timeout while getting quote")
         return None



# PRICE
def get_price(symbol):
    symbol = symbol.upper()
    type = symbol_type(symbol)

    if ( type == "invalid" ):
        return "Please Enter a valid symbol"
    
    if ( type == 'stock' ):
        quote = stock_quote(symbol)
        if ( not( quote )): return "Sorry Something went wrong."
        return f"Last traded price of {symbol} is {quote['priceInfo']['lastPrice']}"

    if ( type == 'index' ):
        quote = index_quote(symbol)
        if ( not(quote) ): return "Sorry something went wrong"
        if (market_status() == "closed"):
            return f"Closing price of {symbol} is {quote['closePrice']}"
        # else:
            # ?????  Extract Price when market is open ??????????



# MARKET
def market_status():
# //////////////////
# ?????  get Market status using api ??????????
    return "closed"
# //////////////////



# SYMBOL
def symbol_type(symbol):
    symbol = symbol.upper()

    if (symbol in INDEX_LIST):
        return "index"
    if (symbol in STOCK_LIST):
        return "stock"

    return "invalid"