from secret import ACCESS_TOKEN, SECRET_KEY
from account import Account

import random
import time

"""
Monkey is a dumb bot.
Every interval, It will try to sell or buy maximum amount of coins.
Since balance arithmetic is not accurate, error will be increased in a
long term.

Use it at your own risk. This script can destroy your account!

example output:
    {'krw': 2, 'btc': 0.0, 'eth': 0.0519324}
    {'krw': 2, 'btc': 0.0, 'eth': 0.0519324}
    {'krw': 2, 'btc': 0.0, 'eth': 0.0519324}
    {'krw': 2979, 'btc': 0.0, 'eth': 0.0001323999999999978}
    {'krw': 2979, 'btc': 0.0, 'eth': 0.0001323999999999978}
    {'krw': 2979, 'btc': 0.0, 'eth': 0.0001323999999999978}
    {'krw': 2979, 'btc': 0.0, 'eth': 0.0001323999999999978}
    {'krw': 6, 'btc': 0.0, 'eth': 0.05146558}
    {'krw': 2968, 'btc': 0.0, 'eth': 6.557999999999564e-05}
    {'krw': 5, 'btc': 0.0, 'eth': 0.05129888999999999}
    {'krw': 5, 'btc': 0.0, 'eth': 0.05129888999999999}
    {'krw': 5, 'btc': 0.0, 'eth': 0.05129888999999999}
    {'krw': 2958, 'btc': 0.0, 'eth': 9.888999999999037e-05}
    {'krw': 2958, 'btc': 0.0, 'eth': 9.888999999999037e-05}
    {'krw': 1, 'btc': 0.0, 'eth': 0.05123232999999999}
    {'krw': 1, 'btc': 0.0, 'eth': 0.05123232999999999}
    {'krw': 2948, 'btc': 0.0, 'eth': 0.000132329999999993}
    {'krw': 2948, 'btc': 0.0, 'eth': 0.000132329999999993}
    {'krw': 0, 'btc': 0.0, 'eth': 0.05106602999999999}
    {'krw': 0, 'btc': 0.0, 'eth': 0.05106602999999999}
    {'krw': 2941, 'btc': 0.0, 'eth': 6.60299999999947e-05}
"""


class Monkey:
    def __init__(self, target='eth', budget=3000, interval=10, account=None):
        """
        limiting it's budget so that it dose not consume all my account balance
        """
        self.balance = {
            'krw': budget,
            'btc': 0.0,
            'eth': 0.0,
        }
        self.target = target
        self.account = account
        self.interval = interval

    def start_working(self):
        for _ in range(20):
            try:
                random.choice([self.buy, self.sell])()
            except Exception as e:
                #  print(e.args)
                pass
            self.report()
            time.sleep(self.interval)

        self.sell()  # exiting with selling all remainig coins
        self.report()

    def sell(self):
        qty = self.balance[self.target]
        res = self.account.sell(currency=self.target, qty=round(qty-0.0001, 4))
        self.update_balance(res['orderId'])

    def buy(self):
        price = self.balance['krw']
        res = self.account.buy(currency=self.target, price=price)
        self.update_balance(res['orderId'])

    def update_balance(self, order_id):
        time.sleep(1)  # wait until the deal is established
        orders = self.account.complete_orders(self.target)
        res = next(filter(lambda o: o['orderId'] == order_id.upper(), orders))
        price, qty, fee = float(res['price']), float(res['qty']), float(res['fee'])
        if res['type'] == 'bid':
            self.balance['krw'] -= round(price*qty)
            self.balance[self.target] += qty - fee
        else:
            self.balance['krw'] += round(price*qty-fee)
            self.balance[self.target] -= qty

    def report(self):
        print(self.balance)


if __name__ == "__main__":
    account = Account(ACCESS_TOKEN, SECRET_KEY)
    monkey = Monkey(account=account)
    monkey.start_working()
