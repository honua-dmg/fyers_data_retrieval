
from fyers_apiv3.FyersWebsocket import data_ws

import datetime as dt
import os


class _Data():
    def __init__(self,access_token:str,stonks:list,directory = None):
        self.access_token = access_token
        self.stonks = stonks # list of stonks in "NSE:SBIN-EQ" this format
        self._initialised = False
        self._connected = False
        self._litemode = False
        self.data_type = None # defined in subclasses
        self.keys = None
        if directory == None:
            self.dir = r'/Users/gurusai/data'
        else:
            self.dir = directory
        #datetime in YYYY-MM-DD format
        self.india_date = dt.datetime.strftime(dt.datetime.now(dt.UTC) + dt.timedelta(hours=5.5),"%Y-%m-%d")


    def initDirFiles(self):
   
        for stonk in self.stonks:
            #check if directories exist
            file_symbol = ''.join(['-' if x == ":" else x for x in stonk])
            if not os.path.exists(f'{self.dir}/{file_symbol}'): #checking to see if file path exists
                try:
                    os.mkdir(f'{self.dir}/{file_symbol}')           #we will make the file path if it doesnt :)
                except Exception:
                    print('file already exists')
            #check if file with type and datestamp is initialised
            file_path = f'{self.dir}/{file_symbol}/{self.data_type[:4]}-{self.india_date}.csv'
            self.initcols(file_path)


    def initcols(self,file_path):

        with open(file_path,'a+') as f:
            if os.path.getsize(file_path) != 0:  #if file is already made, no need to initialse it again
                return
           
            for key in self.keys:
                f.write(key+',')
            f.write('time')
            f.write('\n')




    def onmessage(self,message):
        if self._connected == False:
            self.fyers.unsubscribe(symbols=self.stonks, data_type=self.data_type)
        print("Response:", message)
        self.save_files(message)

    def onerror(self,message):
        print("Error:", message)
       
    def onclose(self,message):
        print("Connection closed:", message)

    def onopen(self):
        print('connection opened')
   
    def connect(self):
        self.fyers  = data_ws.FyersDataSocket(
        access_token=self.access_token,       # Access token in the format "appid:accesstoken"
        log_path='',                     # Path to save logs. Leave empty to auto-create logs in the current directory.
        litemode=self._litemode,                  # Lite mode disabled. Set to True if you want a lite response.
        write_to_file=False,              # Save response in a log file instead of printing it.
        reconnect=True,                  # Enable auto-reconnection to WebSocket on disconnection.
        on_connect=self.onopen,               # Callback function to subscribe to data upon connection.
        on_close=self.onclose,                # Callback function to handle WebSocket connection close events.
        on_error=self.onerror,                # Callback function to handle WebSocket errors.
        on_message=self.onmessage,            # Callback function to handle incoming messages from the WebSocket.
        reconnect_retry=10               # Number of times reconnection will be attepmted in case
        )
        self.fyers.connect()
        self._initialised = True

    def save_files(self,message):
        india_epoch = (dt.datetime.now(dt.UTC) + dt.timedelta(hours=5.5)).timestamp()
        if 'symbol' not in message.keys(): # a message without data
            return
       
        del message['type'] # we don't need it
        file_symbol = ''.join(['-' if x == ":" else x for x in message.pop('symbol')])
        file_path = f'{self.dir}/{file_symbol}/{self.data_type[:4]}-{self.india_date}.csv'


        with open(file_path,'a+') as f:
            for key in message:
                f.write(str(message[key])+',')
            f.write(str(india_epoch))
            f.write('\n')

    def subscribe(self):
        #data type: DepthUpdate, SymbolUpdate
        if self._initialised:
            self.fyers.subscribe(symbols=self.stonks,data_type=self.data_type)
            self.fyers.keep_running()
            self._connected = True
        else:
            print(f'initialise websocket via .connect()')

    def unsubscribe(self):
        if self._connected:
            self.fyers.unsubscribe(symbols=self.stonks, data_type=self.data_type)
            self._connected=False # not having this seems to cause some bugs (i.e it wont unsubscribe)


   
class Depth(_Data):
    def __init__(self,access_token,stonks,directory=None):
        super().__init__(access_token=access_token,stonks=stonks,directory=directory)
        self.keys = ['bid_price1','bid_price2','bid_price3','bid_price4','bid_price5',
                    'bid_size1','bid_size2','bid_size3','bid_size4','bid_size5',
                    'bid_order1','bid_order2','bid_order3','bid_order4','bid_order5',
                    'ask_price1','ask_price2','ask_price3','ask_price4','ask_price5',
                    'ask_size1','ask_size2','ask_size3','ask_size4','ask_size5',
                    'ask_order1','ask_order2','ask_order3','ask_order4','ask_order5']
        self.data_type = 'DepthUpdate'
        self.initDirFiles()
        def onmessage(self, message):
            print("RESPONSE:",message)
            self.save_files(message)


class Symbol(_Data):
    def __init__(self,access_token,stonks,directory=None,litemode=False):
        super().__init__(access_token=access_token,stonks=stonks,directory=directory)
        self.keys =   ['ltp', 'vol_traded_today', 'last_traded_time', 'exch_feed_time', 'bid_size', 'ask_size',
                        'bid_price', 'ask_price', 'last_traded_qty', 'tot_buy_qty', 'tot_sell_qty', 'avg_trade_price',
                        'low_price','high_price', 'lower_ckt', 'upper_ckt', 'open_price', 'prev_close_price', 'ch', 'chp']
        self.data_type = 'SymbolUpdate'
        self._litemode=litemode
        self.initDirFiles()
    
    def onmessage(self, message):
        print("RESPONSE:",message)
        self.save_files(message)


if __name__ =="__main__":
    test = Depth('lalala',['hello'])
    print('helloss')