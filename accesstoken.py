from fyers_apiv3 import fyersModel
import webbrowser as web
import datetime as dt
import os


"""
def access_token(client_id,secret_key, redirect_uri,auth_code):
    grant_type = "authorization_code"
    session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
    )
    # Set the authorization code in the session object
    session.set_token(auth_code)
    # Generate the access token using the authorization code
    response = session.generate_token()
    print(response['code'])
    if response['s']=='ok':
        return response['access_token']
    else:
        return NotImplementedError('bro you fucked up somewhere')
   
"""


class initial():
    def __init__(self,client_id,secret_key, redirect_uri):
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.response_type = "code"  
        self.state = "sample_state"
        self.grant_type = "authorization_code"
        self.auth_code = ''
        self.access_token = ''


    def get_access_token(self):
        """gives us access token"""


        """ gets auth_code"""
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type=self.response_type,
            grant_type=self.grant_type
        )
       


        # Generate the auth code using the session model
        response = session.generate_authcode()
        web.open_new_tab(response)
        with open(r"C:\Users\gurus\Desktop\programming\stonks\django_test\auth.txt",'r+') as f:
            self.auth_code = f.readline()
            f.truncate(0)
        print('successfully obtained auth_code!')
       
        """outputs access token """
        # Set the authorization code in the session object
        session.set_token(self.auth_code)
        # Generate the access token using the authorization code
        response = session.generate_token()
        print(response['code'])
        if response['s']=='ok':
            self.access_token = response['access_token']
            print('*'*80)
            print('success')
            return self.access_token
        else:
            return NotImplementedError('bro you fucked up somewhere'+response['code'])
       


       


if __name__ == '__main__':
    client_id = "8VRFT7VQY2-100"
    secret_key = "BX697QBUL1"
    redirect_uri = 'http://127.0.0.1:8000/eg/'#"https://trade.fyers.in/api-login/redirect-uri/index.html"
    state = "sample_state"
    connect = initial(client_id=client_id,secret_key=secret_key,redirect_uri=redirect_uri)
    connect.get_access_token()
    #print(connect.access_token)



