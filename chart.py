import logging
import httplib2
import simplejson as json
from common import error_code
from operator import itemgetter
import pandas as pd

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)


def raw_data(currency='btc', period='day'):
    def eval(data):
        """ Convert fetched data to navtive types """
        return {'price': int(data['price']),
                'qty': float(data['qty']),
                'timestamp': int(data['timestamp'])}

    url = 'https://api.coinone.co.kr/trades/?currency={}&period={}&format=json&'.format(currency, period)
    http = httplib2.Http()
    response, content = http.request(url, 'GET')
    res = json.loads(content)

    # raise error if fetching is failed.
    if res['result'] != 'success':
        err = res['errorCode']
        logger.error('Failed to get chart data: %d %s' % (int(err), error_code[err]))
        raise Exception(int(err), error_code[err])

    # just make it sure that result is sorted by timestamp.
    return sorted(map(eval, res['completeOrders']), key=itemgetter('timestamp'))


def get_data(currency='btc', period='day', interval=60*15):
    raw = raw_data(currency, period)
    inf = 1e60
    ret = []
    now = raw[-1]['timestamp']

    def new_data(timestamp):
        return {'timestamp': timestamp,
                'high': -inf, 'low': inf, 'qty': 0, 'close': -1, 'open': -1}

    data = new_data(now)
    prev = None
    while raw:
        last = raw.pop()
        if now - last['timestamp'] > interval:
            data['open'] = prev['price']
            ret.append(data)
            now -= interval
            data = new_data(now)
        if data['close'] == -1:
            data['close'] = last['price']
        data['high'] = max(data['high'], last['price'])
        data['low'] = min(data['low'], last['price'])
        data['qty'] += last['qty']
        prev = last
    return pd.DataFrame(list(reversed(ret)))


if __name__ == "__main__":
    print(get_data())
