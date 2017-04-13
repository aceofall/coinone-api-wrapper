import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time

base_url = 'https://api.coinone.co.kr/v2/'
error_code = {
    '11':	"Access token is missing",
    '12':	"Invalid access token",
    '40':	"Invalid API permission",
    '50':	"Authenticate error",
    '51':	"Invalid API",
    '100': "Session expired",
    '101': "Invalid format",
    '102': "ID is not exist",
    '103': "Lack of Balance",
    '104': "Order id is not exist",
    '105': "Price is not correct",
    '106': "Locking error",
    '107': "Parameter error",
    '111': "Order id is not exist",
    '112': "Cancel failed",
    '113': "Quantity is too low(ETH, ETC > 0.01)",
    '120': "V2 API payload is missing",
    '121': "V2 API signature is missing",
    '122': "V2 API nonce is missing",
    '123': "V2 API signature is not correct",
    '130': "V2 API Nonce value must be a positive integer",
    '131': "V2 API Nonce is must be bigger then last nonce",
    '132': "V2 API body is corrupted",
    '150': "It's V1 API. V2 Access token is not acceptable",
    '151': "It's V2 API. V1 Access token is not acceptable",
    '200': "Wallet Error",
    '202': "Limitation error",
    '210': "Limitation error",
    '220': "Limitation error",
    '221': "Limitation error",
    '310': "Mobile auth error",
    '311': "Need mobile auth",
    '312': "Name is not correct",
    '330': "Phone number error",
    '404': "Page not found error",
    '405': "Server error",
    '444': "Locking error",
    '500': "Email error",
    '501': "Email error",
    '777': "Mobile auth error",
    '778': "Phone number error",
    '1202': "App not found",
    '1203': "Already registered",
    '1204': "Invalid access",
    '1205': "API Key error",
    '1206': "User not found",
    '1207': "User not found",
    '1208': "User not found",
    '1209': "User not found"
}


class Account:
    def __init__(self, token, key):
        self.token = token
        self.key = key

    def default_payload(self):
        return {"access_token": self.token}

    def default_post(self, url):
        res = get_response(base_url+url, self.default_payload(), self.key)
        res = json.loads(res)
        if res['errorCode'] != '0':
            raise Exception(error_code[res['errorCode']])
        return json.loads(res)

    def info(self):
        return self.default_post('account/user_info')

    def balance(self):
        return self.default_post('account/balance')

    def daily_balance(self):
        return self.default_post('account/daily_balance')

    def deposit_address(self):
        return self.default_post('account/deposit_address')

    def virtual_account(self):
        return self.default_post('account/virtual_account')


def get_response(url, payload, key):
    def encode_payload(payload):
        payload[u'nonce'] = int(time.time()*1000)
        ret = json.dumps(payload).encode()
        return base64.b64encode(ret)

    def get_signature(encoded_payload, secret_key):
        signature = hmac.new(
            secret_key.upper().encode(), encoded_payload, hashlib.sha512)
        return signature.hexdigest()

    encoded_payload = encode_payload(payload)
    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload, key)
    }
    http = httplib2.Http()
    response, content = http.request(
        url, 'POST', headers=headers, body=encoded_payload)
    return content
