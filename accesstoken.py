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
def get_creds(file_loc,data_type):
    creds = {}
    with open(file_loc,'r') as f:
        txt = f.readlines()
        for i in range(len(txt)):
            if data_type in txt[i]:
                creds['TOTPseckey'] = txt[i+1].split('=')[1].strip("\n,")
                creds['key'] = txt[i+2].split('=')[1].strip("\n,")
                creds['phoneno'] = txt[i+3].split('=')[1].strip("\n,")
                creds['client_id'] = txt[i+4].split('=')[1].strip("\n,")
                creds['secret_key'] = txt[i+5].split('=')[1].strip("\n,")
                creds['redirect_uri'] = txt[i+6].split('=')[1].strip("\n,")  
    return creds

class Login():
    def __init__(self,client_id,secret_key, redirect_uri,key=None,phoneno=None,TOTPseckey=None):
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

    def get_response(self):
        
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
        return response

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
        try:
            self.auth_code= self.login_and_get_auth(response)
        except 'ElementNotInteractableException':
            print('shucks login issue occured, we prolly got detected')
            try:
                self.auth_code= self.login_and_get_auth(response,driver_mode=1)
            except Exception:
                print('auth code failed to be received')
                return NotImplementedError('bro SeleniumBase might be failing you look for alternatives')

       
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
            return NotImplementedError('bro you fucked up somewhere'+str(response['code']))
       
    def login_and_get_auth(self,response,driver_mode=0):
        if self.TOTPseckey == None:
            return KeyError('TOTPseckey not provided')
        if self.four_digit_key == None:
            return KeyError('four digit key not provided')
        if self.phoneno == None:
            return KeyError('phoneno not provided')
        try:
            if driver_mode == 0:
                drive = sb.Driver(uc=True)
            elif driver_mode == 1:
                drive = sb.Driver(undetectable=True)
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
                # terms and conditions validation 
                drive.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[3]/div/div[3]/label').click()
                drive.find_element(By.XPATH,'/html/body/div/div/div/div/div/div[4]/div/a[2]/span').click()
            except Exception as e:
                print('no neeed to validate :)')
            time.sleep(2)
            url = drive.current_url
            return url.split('&')[2].split('=')[1]
        finally:
            drive.quit()
        
       
class AutoLogin(Login):
    def __init__(self,file_loc,data_type):
        creds = get_creds(file_loc=file_loc,data_type=data_type)
        super().__init__(client_id=creds['client_id'],
                         secret_key=creds['secret_key'],
                         redirect_uri=creds['redirect_uri'],
                         key=creds['key'],
                         phoneno=creds['phoneno'],
                         TOTPseckey=creds['TOTPseckey'])


def auth_codes(file_loc):
    sym_auth = AutoLogin(file_loc=file_loc,data_type='symbol').login_and_get_auth()
    dep_auth = AutoLogin(file_loc=file_loc,data_type='depth').login_and_get_auth()

    return {'depth':dep_auth,'symbol':sym_auth}
#client_id,secret_key, redirect_uri,key=None,phoneno=None,TOTPseckey=None






if __name__ == '__main__':
    client_id = "8VRFT7VQY2-100"
    secret_key = "BX697QBUL1"
    redirect_uri = 'https://www.google.com/'#"https://trade.fyers.in/api-login/redirect-uri/index.html"
    state = "sample_state"
    connect = Login(client_id=client_id,secret_key=secret_key,redirect_uri=redirect_uri)
    connect.get_access_token()
    #print(connect.access_token)



