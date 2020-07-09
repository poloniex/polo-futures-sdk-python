# Copyright 2020 Polo Digital Assets, Ltd.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import os

from polofutures import RestClient


# Account Keys
API_KEY = os.environ['PF_API_KEY']
SECRET = os.environ['PF_SECRET']
API_PASS = os.environ['PF_PASS']

rest_client = RestClient(API_KEY, SECRET, API_PASS)

SYMBOL = 'BTCUSDTPERP'


# Fetch MarketData
market = rest_client.market_api()

server_time = market.get_server_timestamp()
l3_depth = market.get_l3_order_book(SYMBOL)
l2_depth = market.get_l2_order_book(SYMBOL)
klines = market.get_ticker(SYMBOL)


# Trade Functions
trade = rest_client.trade_api()

order_id = trade.create_limit_order(SYMBOL, 'buy', '1', '30', '8600')
cancel_id = trade.cancel_order(order_id['orderId'])
order_id = trade.create_limit_order(SYMBOL, 'buy', '1', '30', '8600')
cancel_all = trade.cancel_all_limit_orders(SYMBOL)


# User Account Functions
user = rest_client.user_api()

account_overview = user.get_account_overview()
