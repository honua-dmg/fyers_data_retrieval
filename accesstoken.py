from fyers_apiv3 import fyersModel

import seleniumbase as sb
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pyotp


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
    def __init__(self,client_id,secret_key, redirect_uri,key:str,phoneno:str,TOTPseckey:str):
        self.client_id = client_id
        self.secret_key = secret_key
        self.redirect_uri = redirect_uri
        self.four_digit_key = key
        self.phoneno = phoneno
        self.TOTPseckey = TOTPseckey
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
        drive = sb.Driver(uc=True)
        drive.get(response)
        time.sleep(2)
        #clicking on phone number box
        phno = drive.find_element(By.XPATH,'/html/body/section[1]/div[3]/div[3]/form/div[1]/div/input')
        phno.click()
        #sending phone number details
        phno.send_keys(self.phoneno)

        #clicking on continue
        drive.find_element(By.XPATH,'/html/body/section[1]/div[3]/div[3]/form/button').click()
        time.sleep(3)
        #sending TOTP 
        otp = pyotp.TOTP(self.TOTPseckey).now()
        for i in range(1,7):
            drive.find_element(By.XPATH,f'/html/body/section[6]/div[3]/div[3]/form/div[3]/input[{i}]').send_keys(otp[i-1])

        #pressing continue
        drive.find_element(By.XPATH,'/html/body/section[6]/div[3]/div[3]/form/button').click()
        time.sleep(3)
        #sending id

        for i in range(1,5):
            drive.find_element(By.XPATH,f'/html/body/section[8]/div[3]/div[3]/form/div[2]/input[{i}]').send_keys(self.four_digit_key[i-1])
        drive.find_element(By.XPATH,'/html/body/section[8]/div[3]/div[3]/form/button').click()
        try:
            drive.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[3]/div/div[3]/label').click()
            drive.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[4]/div/a[2]/span').click()
        except Exception as e:
            pass
        time.sleep(2)
        url = drive.current_url
        self.auth_code = url.split('&')[2].split('=')[1]


        drive.close()
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
    redirect_uri = 'https://www.google.com/'#"https://trade.fyers.in/api-login/redirect-uri/index.html"
    state = "sample_state"
    connect = initial(client_id=client_id,secret_key=secret_key,redirect_uri=redirect_uri)
    connect.get_access_token()
    #print(connect.access_token)



