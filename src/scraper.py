# Model
import yfinance

class Company(yfinance.Ticker):
    
    def get_profile():
        '''
        return the first two setnences of ticker.info["longBusinessSummary"]
        https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences
        '''
