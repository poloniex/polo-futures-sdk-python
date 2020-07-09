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

from polofutures.rest.market import MarketClient
from polofutures.rest.trade import TradeClient
from polofutures.rest.user import UserClient


class RestClient:
    def __init__(self, key=None, secret=None, passphrase=None, base_url=None):
        self._user_client = UserClient(key, secret, passphrase, base_url)
        self._trade_client = TradeClient(key, secret, passphrase, base_url)
        self._market_client = MarketClient(key, secret, passphrase, base_url)

    def user_api(self):
        return self._user_client

    def trade_api(self):
        return self._trade_client

    def market_api(self):
        return self._market_client
