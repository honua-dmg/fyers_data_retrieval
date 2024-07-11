""" 
from data import Depth,Symbol
import time

symbol_access = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjA1OTQ1OTIsImV4cCI6MTcyMDY1NzgzMiwibmJmIjoxNzIwNTk0NTkyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbWpqQ2dpb0tZVUdfdkJsUlM0Y0J2UEJ0emYyQ2tlVWk1VE5EVFl4a1k4SVZINGdsNXRsVzlKWDJybW0yNFJSS3NWNmVOYmttZlhzQWNYUW1VU1VVODhwXzZPWWotX2VxU3Y0NmtzZWl1b2FpRzI2ND0iLCJkaXNwbGF5X25hbWUiOiJNQUxMRVBBTExJIEdBSlVMQSBHVVJVIFNBSSBQUkFTQUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjY2Q4NDkwZGNkYTc2OTU0Njk3YmE4Y2JkN2YxMGI5MWNjMTU1YmI2ODA5OGRkZjUxYjk0NTg5ZiIsImZ5X2lkIjoiWU0wODkyNyIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.XkKx8VcIvFu2yPAY2WeC_vYHJ1f3KSrcnmneVbjUVv4'
depth_access = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjA1OTQ2MDcsImV4cCI6MTcyMDY1Nzg0NywibmJmIjoxNzIwNTk0NjA3LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbWpqQ3ZIYmFsWGFKTmVERlBGRGFmSEJaajZncmxuY2ZhQkpEbEh2VmIxTXAya0k5a2FwbmlsOVNNLWgwV3VIQmYzb3pJcDh0cmhuVjA5VnZzNWJaTXgxM3ZMczhvb2JlSGxncVlCYk40aFk5Zi15MD0iLCJkaXNwbGF5X25hbWUiOiJNQUxMRVBBTExJIEdBSlVMQSBHVVJVIFNBSSBQUkFTQUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjY2Q4NDkwZGNkYTc2OTU0Njk3YmE4Y2JkN2YxMGI5MWNjMTU1YmI2ODA5OGRkZjUxYjk0NTg5ZiIsImZ5X2lkIjoiWU0wODkyNyIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.QypnBnF9c5MEWCWnYB7V6HzuR5o9R0UM9SHAKozNmoY'

depth = Depth(depth_access,['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ'])
symbol = Symbol(symbol_access,['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ'])

depth.connect()
symbol.connect()

depth.subscribe()
symbol.subscribe()

time.sleep(10)
depth.unsubscribe()
symbol.unsubscribe()"""
import concurrent.futures
from data import Depth,Symbol
import time
def process(type,auth_code,stonks:list,time):
    access = auth_code
    data = type(access,stonks)
    data.connect()
    data.subscribe()
    time.sleep(time)
    data.unsubscribe()

with concurrent.futures.ProcessPoolExecutor() as exec:
    if __name__=="__main__":
        exec.submit(process,[Depth,
                            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjA1OTQ2MDcsImV4cCI6MTcyMDY1Nzg0NywibmJmIjoxNzIwNTk0NjA3LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbWpqQ3ZIYmFsWGFKTmVERlBGRGFmSEJaajZncmxuY2ZhQkpEbEh2VmIxTXAya0k5a2FwbmlsOVNNLWgwV3VIQmYzb3pJcDh0cmhuVjA5VnZzNWJaTXgxM3ZMczhvb2JlSGxncVlCYk40aFk5Zi15MD0iLCJkaXNwbGF5X25hbWUiOiJNQUxMRVBBTExJIEdBSlVMQSBHVVJVIFNBSSBQUkFTQUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjY2Q4NDkwZGNkYTc2OTU0Njk3YmE4Y2JkN2YxMGI5MWNjMTU1YmI2ODA5OGRkZjUxYjk0NTg5ZiIsImZ5X2lkIjoiWU0wODkyNyIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.QypnBnF9c5MEWCWnYB7V6HzuR5o9R0UM9SHAKozNmoY',
                            ['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ'],
                            10])
        exec.submit(process,[Symbol,
                            'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjA1OTQ1OTIsImV4cCI6MTcyMDY1NzgzMiwibmJmIjoxNzIwNTk0NTkyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbWpqQ2dpb0tZVUdfdkJsUlM0Y0J2UEJ0emYyQ2tlVWk1VE5EVFl4a1k4SVZINGdsNXRsVzlKWDJybW0yNFJSS3NWNmVOYmttZlhzQWNYUW1VU1VVODhwXzZPWWotX2VxU3Y0NmtzZWl1b2FpRzI2ND0iLCJkaXNwbGF5X25hbWUiOiJNQUxMRVBBTExJIEdBSlVMQSBHVVJVIFNBSSBQUkFTQUQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiJjY2Q4NDkwZGNkYTc2OTU0Njk3YmE4Y2JkN2YxMGI5MWNjMTU1YmI2ODA5OGRkZjUxYjk0NTg5ZiIsImZ5X2lkIjoiWU0wODkyNyIsImFwcFR5cGUiOjEwMCwicG9hX2ZsYWciOiJOIn0.XkKx8VcIvFu2yPAY2WeC_vYHJ1f3KSrcnmneVbjUVv4',
                            ['NSE:SBIN-EQ','BSE:SBIN-A','NSE:TATAMOTORS-EQ'],
                            10])