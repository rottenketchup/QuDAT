from plotting import files
from data import Stream
import csv
from time import sleep

def parse_and_act():
    global string

    # remove redundant words from global variable string
    shorten(redundant_words)
    if diagnostics:
        print("Shortened: " + string)

    # identify the first phrase corresponding with an "intent", save the intent in key_word using pre-existing macros, 
    # and remove the phrase from string
    key_word = find_and_remove_key_word()
    if diagnostics:
        print("Keyword: " + str(key_word)) #str(key_word) as the return type can be None
        print("Keyword-removed string: " + string)

    # remove any remaining intent-phrases
    shorten_further()
    if diagnostics:
        print("Further shortened: " + string)

    # acquire the company's ticker symbol
    symbol = get_symbol()
    if diagnostics:
        print("Ticker: " + symbol + "\n")

    obj = Stream(symbol) # initialize the web-scraper
    action(obj, key_word) # execute the action


def shorten(corpus):
    global string
    string = string.replace("?", "")

    new_string = []
    for word in string.split():
        if not word in corpus and not (word[::-1].replace("s", "", 1))[::-1] in corpus:
            new_string.append(word)
    string = " ".join(new_string)


def find_and_remove_key_word():
    global pairs, string
    
    for key in pairs.keys():
        plural = key + 's'
        if len(key) == 1 and (set([key]).issubset(set(string.split())) or set([plural]).issubset(set(string.split()))) or (set(key.split()).issubset(set(string.split())) or set(plural.split()).issubset(set(string.split()))):
        #if set([key]).issubset(set(string.split())) or set([plural]).issubset(set(string.split())):
            if plural in string.split():
                string = string.replace(plural, "", 1)
            else:
                string = string.replace(key, "", 1)
            return pairs[key]


def shorten_further():
    shorten(corpus=second_order_redundants)    


def initialize_definitions():
    '''
    Initializes all macros needed by other functions
    '''

    #every word's plural is also accounted for by the algorithms
    #SUPERSTRINGS MUST PRECEDE SUBSTRINGS!!

    #key_word type declarations
    global p, r, i, f, qf, bc, cf, fcf, eb, m, pe, eps, cap, vol
    p     = "price"
    r, i  = "revenue", "income"
    f, qf = "financials", "quarterly_financials"
    bc    = "balance_sheet"
    cf    = "cashflow"
    fcf   = "fcf"
    eb    = "ebitda"
    m     = "margins"
    pe    = "PE ratio"
    eps   = "EPS"
    cap   = "market capitalization"
    vol   = "volume"

    global redundant_words # for shorten()
    redundant_words = ['information', 'moment', "how's", 'who', "what's", 'what', 'was', 'when', 'why', 'show', 'how', 'of', 'is', 
    'much', 'worth', 'bring', 'me', 'find', 'search', 'can', 'you', 'does', 'do', 'make', 'think', 'know', 'fetch', 'get', 'look', 
    'suppose', 'for', 'tell', 'right', 'now', 'database', 'the', 'up', 'contain', 'help', 'please', 'in', 'about', 'at', 'number', 
    'business']

    global second_order_redundants # for shorten_further()
    second_order_redundants = ['stock', 'price', 'share', 'revenue', 'sale', 'net', 'income', 'profit', 'earning', 'financial', 
    'statement', 'report', 'quarterly', 'of', 'cashflow', 'cash', 'flow', 'balance', 'sheet', 'free', 'fcf', 'ebitda', 
    'ebit', 'margin', 'gross', 'operating', 'per', 'ratio', 'p/e', 'to', 'by', 'eps', 'pe', 'market', 'capitalization', 'cap', 
    'volume', 'daily', 'traded', 'annual', 'trade', 'vol', '/']

    global pairs # for find_and_remove_key_word()
    pairs = {
        "price":p,

        "margin":m,

        "revenue":r, "sale":r,
        "income":i, "profit":i, "loss":i,

        "quarterly":qf,
        "earning":f, "financial":f,

        "free cash flow": fcf, "free cashflow": fcf, "fcf": fcf,

        "cash flow":cf, "cashflow":cf,

        "balance":bc,

        "ebitda": eb, "ebit":eb,

        "pe ratio":pe, "p/e":pe, 

        "eps":eps, "earnings per share":eps,

        "market cap":cap, "market capitalization":cap, "capitalization":cap,

        "volume":vol, 

        "stock":p, "share":p,
    }


def get_symbol():
    '''
    Searches for ticker symbols across local files.
    It is assumed that global variable string only contains the company's name by this point.
    If a match is not found, an exception is thrown with the following message:
    "The given company's ticker symbol could not be found!"
    '''
    global string 
    string = string.strip().upper()

    hit = search(string, "NIFTY.csv")
    if hit != None:
        return hit.replace("/", ".") + ".NS"

    hit = search(string, "NASDAQ.csv")
    if hit != None:
        return hit.replace("/", ".")

    hit = search(string, "NSE.csv")
    if hit!= None:
        return hit.replace("/", ".") +".NS"

    raise Exception("The given company's ticker symbol could not be found!") 


def search(string, file_name):
    '''
    Searches for ticker symbols for a given company in a mentioned file, returns None if no match is found,
    otherwise the first match's ticker is returned.

    Arguments:
    param string -- company name in uppercase (search is case-insensitive)
    file_name -- the stock's exchange respective lister of tickers

    It is assumed that the first column contains ticker symbols, while the second column contains names.
    The absence of names in the second column will not lead to any issues so as long there is a second column.

    matching priority:
    * Ticker symbol is an exact match OR
    * Name contains exact phrase in user-defined case, separated from other phrases in the cell by spaces
    '''
    match = None
    with open(file_name, "r") as file:
        reader = csv.reader(file)
        for line in reader:
            if len(line) > 1:
                if string == line[0].upper():
                    match = string
                    break
                elif set(string.split()).issubset(line[1].upper().split()):
                    match = line[0]
                    break
    if diagnostics and match != None:
        print("Found in " + file_name)
    return match


def action(obj, key_word):
    print()
    if key_word == p:
        print(obj.get_price())
        prepare_for_plotting(obj.retrieve_prices()) #OVER TO SHRESHTH
    elif key_word == r:
        print(obj.get_revenue())
    elif key_word == i:
        print(obj.get_income())
    elif key_word == qf or key_word == f:
        if input("| Type S for simplified-income statment, hit enter otherwise\n: ").upper() == "S":
            print("\n" + obj.get_earnings())
        elif key_word == f:
            print("\n" + obj.get_financials())
        elif key_word == qf:
            print(obj.get_financials(is_quarterly=True))
    elif key_word == bc:
        print(obj.get_balance_sheet())
    elif key_word == cf:
        print(obj.get_cashflow())
    elif key_word == fcf:
        print(obj.get_fcf())
    elif key_word == eb:
        print(obj.get_ebitda())
    elif key_word == m:
        print(obj.get_margins())
    elif key_word == pe:
        print(obj.get_pe())
    elif key_word == eps:
        print(obj.get_eps())
    elif key_word == cap:
        print(obj.get_market_cap())
    elif key_word == vol:
        print(obj.get_volume())


def prepare_for_plotting(csv_file):
    with open("output.csv", "w") as file:
        file.write(csv_file)
        files() 


if __name__ == "__main__":
    initialize_definitions()
    string = ""
    diagnostics = False

    if input("Enter D to run in diagnostics-mode: ") == "D":
        diagnostics = True

    while True:
        try:
            sleep(0.1) #short delay to avoid registering any pre-existing text in the terminal as input
            string = input("\n\n: ").lower()
            if string != "" and ".PY" not in string and not ".py" in string:
                parse_and_act()
        except Exception as err:
            if diagnostics:
                print("| The request was terminated.", err, sep="\n")
