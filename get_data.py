import multiprocessing
from data import Depth,Symbol, collect
from accesstoken import auth_codes
import time
"""
#stonk list 
#TODO: figureout what stonks I want data on (25 stocks listed on BSE and NSE)
stonks = ['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ']
wait_time = 60*60*6

#get access token:
#TODO: randomise getting these codes in between the timeframe 8am to 8:30am
try:
    auth_codes = auth_codes('secrets.txt')
except Exception as e:
    print(f"SOMETHING WENT WRONG: BEEP BEEP BEEP {e}")

# connect to fyers websocket
depth = collect(Depth,auth_codes['depth'],stonks=stonks,wait_time=wait_time)
symbol = collect(Symbol,auth_codes['symbol'],stonks,wait_time=wait_time)
"""

class Connect():
    def __init__(self,stonks=['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ'],wait_time=60*60*6,file_loc = 'secrets.txt') -> None:
        self.stonks=stonks
        self,wait_time=wait_time
        self.file_loc = file_loc
        self.access_codes = {}

    def get_access_codes(self):
        self.access_codes = auth_codes(self.file_loc)
    
    def connect(self):
        depth = collect(Depth,self.access_codes['depth'],stonks=self.stonks,wait_time=self.wait_time)
        symbol = collect(Symbol,self.access_codes['symbol'],self.stonks,wait_time=self.wait_time)