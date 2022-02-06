import yfinance as yf

class Stream:

    parameters = {}

    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self.initialize_parameters()

    def get_columns(self, raw_data, list_of_col, remove_zeroes=False): #filters empty rows, empty line at end
        clean_data = ""

        for line in raw_data.split('\n'):
            if line != "":
                row= line.split(",")
                if not None in row and not "" in row and row != []:
                    if remove_zeroes==True and 0 in row:
                        pass
                    else:
                        clean_data += "| " + ", ".join([str(row[i]) for i in list_of_col])+"\n"

        return clean_data


    def presentable_numbers(self, clean_data):
        return (clean_data[::-1].replace("000000000", " B").replace("000000", " M").replace("000", " K"))[::-1]


    def add_thousandth_sep(self, value):
        return f'{value:,}'


    def initialize_parameters(self):
        try:
            self.currency = self.stock.info["financialCurrency"]
            self.cur_string = "| (All in " + self.currency + ")"
        except:
            self.currency = ""
            self.cur_string = ""
        
        #self.name = self.stock.info["shortName"]
        #self.location = self.stock.info["city"] + ", " + self.stock.info["country"]


    def retrieve_prices(self, data_interval="1mo"):
        raw_data = self.stock.history(period="max", interval=data_interval).to_csv()
        clean_data = self.get_columns(raw_data,[0, 4])
        return clean_data

    def get_price(self):
        current = self.stock.info["currentPrice"]
        previous = self.stock.info["previousClose"]

        if current < previous:
            up_or_down = " (down " + str(round((1 - current/previous)*100, 2)) + "%)"
        elif current > previous:
            up_or_down = " (up " + str(round((current/previous - 1)*100, 2)) + "%)"
        else:
            up_or_down = ""

        string = "| Current price: " + str(current) + " " + self.currency + up_or_down
        return string

    def get_cashflow(self): 
        return self.stock.cashflow.to_csv() + "\n" + self.cur_string

    def get_balance_sheet(self): 
        return self.stock.balance_sheet.to_csv() + "\n" + self.cur_string

    def get_earnings(self):
        reformatted = ""
        for line in self.stock.earnings.to_csv().split("\n"):
            if line != "":
                reformatted = reformatted + "| " + self.presentable_numbers(line.replace(",", ", ")) + "\n"

        return reformatted + self.cur_string

    def get_financials(self, is_quarterly=False):
        if not is_quarterly:
            return self.stock.financials.to_csv() + "\n" + self.cur_string
        else:
            return self.stock.quarterly_financials.to_csv() + "\n" + self.cur_string

    def get_revenue(self):
        raw_data = self.stock.earnings.to_csv()
        clean_data = self.get_columns(raw_data, [0, 1])
        return self.presentable_numbers(clean_data) + self.cur_string

    def get_income(self):
        raw_data = self.stock.earnings.to_csv()
        clean_data = self.get_columns(raw_data, [0, 2])
        return self.presentable_numbers(clean_data) + self.cur_string 

    def get_ebitda(self): 
        return "| " + str(self.stock.info["ebitda"]) + " " + self.currency

    def get_margins(self):
        string = "| Profit margin: " + str(round(self.stock.info["profitMargins"]*100, 2)) + "%" + "\n| Gross margin: " + str(round(self.stock.info["grossMargins"]*100, 2)) + "%"+ "\n| Operating margin: " + str(round(self.stock.info["operatingMargins"]*100, 2)) + "%"
        return string

    def get_fcf(self): 
        return "| " + self.presentable_numbers(self.add_thousandth_sep(self.stock.info["freeCashflow"])) + " " + self.currency

    def get_pe(self):
        string = "| Forward PE: " + str(round(self.stock.info["forwardPE"],2)) + "\n| Trailing PE: " + str(round(self.stock.info["trailingPE"],2))
        return string
    
    def get_eps(self):
        string = "| Froward EPS: " + str(self.stock.info["forwardEps"]) + "\n| Trailing EPS: " + str(self.stock.info["trailingEps"])
        return string

    def get_market_cap(self): 
        return "| " + self.presentable_numbers(str(self.add_thousandth_sep(self.stock.info["marketCap"]))) + " " + self.currency

    def get_volume(self):
        return "| Average daily volume (last 10d): " + self.presentable_numbers(self.add_thousandth_sep(self.stock.info["averageDailyVolume10Day"]))


"""
    def ratios(self):
        return "Return on equity: " + self.stock.info["returnOnEquity"] 
        + "\nDebt to equity: " + self.stock.info["debtToEquity"] 
        + "\nPrice to book ratio: " + self.stock.info["priceToBook"]    

    def get_name(self): #initialized
        return self.name

"""
