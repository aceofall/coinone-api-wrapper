from common import base_url, error_code
import base64
import simplejson as json
import hashlib
import hmac
import httplib2
import time

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
        return res

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
