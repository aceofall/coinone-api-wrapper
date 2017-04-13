from secret import ACCESS_TOKEN, SECRET_KEY
from account import Account
from pprint import pprint

if __name__ == "__main__":
    my = Account(ACCESS_TOKEN, SECRET_KEY)

    # query account informations
    pprint(my.info())
    pprint(my.balance())
    pprint(my.daily_balance())
    pprint(my.deposit_address())
    pprint(my.virtual_account())

    #  complete orders
    pprint(my.complete_orders())       # query for BTC by default
    pprint(my.complete_orders('eth'))  # query for ETH
    pprint(my.complete_orders('bbb'))  # will raise error

    # make some orders with insane values, and cancel them
    my.buy(price=500, qty=1.000)
    my.buy(price=1000, qty=0.001)
    my.sell(price=100000000, qty=0.001)
    print('made 3 orders')
    orders = my.orders()
    pprint(orders)
    my.cancel(**orders[-1])  # cancel the last one
    print('canceled last one')
    pprint(my.orders())
    my.cancel()              # will cancel all orders by default
    print('canceled remaining')
    pprint(my.orders())
