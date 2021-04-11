import jwt
import requests
from sseclient import SSEClient
from urllib.parse import urlencode;

class ChonkMarketApiClient:
    def __init__(self, api_base_url, token, verify_token=True, verbose=True, ssl_verification=False):
        self.api_base_url = api_base_url
        self.verify_token = verify_token
        self.verbose = verbose
        self.ssl_verification = ssl_verification
        self.token = token

    def do_verify_token(self):
        try:
            data = jwt.decode(self.token, options={"verify_signature": False})
            if self.verbose:
                print(data)
            return True
        except:
            print("Failed to Verify JWT token, reach out to support.")

    def make_request(self, url):
        if self.verify_token:
            self.do_verify_token()
        token = f'Bearer {self.token}'
        return requests.get(url, headers={'Authorization': token}, verify=self.ssl_verification)

    def token_test(self):
        resp = self.make_request(f'{self.api_base_url}/v1/verify')
        print(f'[{resp.status_code}] {resp.text}')

    def fetch_tickers(self):
        resp = self.make_request(f'{self.api_base_url}/v1/quote/tickers')
        print(f'[{resp.status_code}] {resp.text}')

    def fetch_quotes(self, symbol, date):
        resp = self.make_request(f'{self.api_base_url}/v1/quote/{symbol}?date={date}').json()
        print(resp)

    def stream_data(self, symbol, testmode, interval=0, date=""):
        if (testmode):
            paramdict = {}
            if (interval > 200):
                paramdict['interval'] = interval
            if (date != ""):
                paramdict['date'] = date
            url = f'{self.api_base_url}/v1/quote/{symbol}/sse/test?' + urlencode(paramdict)
        else:
            url = f'{self.api_base_url}/v1/quote/{symbol}/sse'
        token = f'Bearer {self.token}'
        return SSEClient(url, headers={'Authorization': token}, verify=self.ssl_verification)
