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

from polofutures.rest.core import SendRequest


class MarketClient:
    def __init__(self, key=None, secret=None, passphrase=None, base_url=None):
        self._request = SendRequest(key, secret, passphrase, base_url)

    def get_server_timestamp(self):
        """
        Get the API server time. This is the Unix timestamp."""
        return self._request('GET', '/api/v1/timestamp')

    def get_interest_rate(self, symbol, **kwargs):
        """
        Check interest rate list.

        Param	    Type	Description
        symbol	    String	Symbol of the contract
        startAt	    long	[optional] Start time (milisecond)
        endAt	    long	[optional] End time (milisecond)
        reverse	    boolean	[optional] This parameter functions to judge whether the lookup is reverse. True means “yes”. False means no. This parameter is set as True by default.
        offset	    long	[optional] Start offset. The unique attribute of the last returned result of the last request. The data of the first page will be returned by default.
        forward	    boolean	[optional] This parameter functions to judge whether the lookup is forward or not. True means “yes” and False means “no”. This parameter is set as true by default
        maxCount	int	    [optional] Max record count. The default record count is 10"""

        params = {
            'symbol': symbol
        }
        params.update(kwargs)

        return self._request('GET', '/api/v1/interest/query', params)

    def get_index_list(self, symbol, **kwargs):
        """
        Check index list

        Param	    Type	Description
        symbol	    String	Symbol of the contract
        startAt	    long	[optional] Start time (milisecond)
        endAt	    long	[optional] End time (milisecond)
        reverse	    boolean	[optional] This parameter functions to judge whether the lookup is reverse. True means “yes”. False means no. This parameter is set as True by default
        offset	    long	[optional] Start offset. The unique attribute of the last returned result of the last request. The data of the first page will be returned by default.
        forward	    boolean	[optional] This parameter functions to judge whether the lookup is forward or not. True means “yes” and False means “no”. This parameter is set as true by default
        maxCount	int	    [optional] Max record count. The default record count is 10"""

        params = {
            'symbol': symbol
        }
        params.update(kwargs)

        return self._request('GET', '/api/v1/index/query', params)

    def get_current_mark_price(self, symbol):
        """
        Check the current mark price.

        Param	Type	Description
        symbol	String	Path Parameter. Symbol of the contract"""
        return self._request('GET', f'/api/v1/mark-price/{symbol}/current')

    def get_premium_index(self, symbol, **kwargs):
        """
        Submit request to get premium index.

        Param	    Type	Description
        symbol  	String	Symbol of the contract
        startAt 	long	[optional] Start time (milisecond)
        endAt	    long	[optional] End time (milisecond)
        reverse	    boolean	[optional] This parameter functions to judge whether the lookup is reverse. True means “yes”. False means no. This parameter is set as True by default
        offset	    long	[optional] Start offset. The unique attribute of the last returned result of the last request. The data of the first page will be returned by default.
        forward	    boolean	[optional] This parameter functions to judge whether the lookup is forward or not. True means “yes” and False means “no”. This parameter is set as true by default
        maxCount	int	    [optional] Max record count. The default record count is 10"""

        params = {
            'symbol': symbol
        }
        params.update(kwargs)

        return self._request('GET', '/api/v1/premium/query', params)

    def get_current_fund_rate(self, symbol):
        """
        Submit request to check the current mark price."""
        return self._request('GET', f'/api/v1/funding-rate/{symbol}/current')

    def get_trade_history(self, symbol):
        """
        List the last 100 trades for a symbol."""

        params = {
            'symbol': symbol
        }

        return self._request('GET', '/api/v1/trade/history', params)

    def get_l2_order_book(self, symbol):
        """
        Get a snapshot of aggregated open orders for a symbol.
        Level 2 order book includes all bids and asks (aggregated by price). This level returns only one aggregated size for each price (as if there was only one single order for that price).
        This API will return data with full depth.
        It is generally used by professional traders because it uses more server resources and traffic, and we have strict access frequency control.
        To maintain up-to-date Order Book, please use Websocket incremental feed after retrieving the Level 2 snapshot.
        In the returned data, the sell side is sorted low to high by price and the buy side is sorted high to low by price.
        """

        params = {
            'symbol': symbol
        }

        return self._request('GET', '/api/v1/level2/snapshot', params)

    def get_l2_messages(self, symbol, start, end):
        """
        If the messages pushed by Websocket is not continuous, you can submit the following request and re-pull the data to ensure that the sequence is not missing.
        In the request, the start parameter is the sequence number of your last received message plus 1, and the end parameter is the sequence number of your current received message minus 1.
        After re-pulling the messages and applying them to your local exchange order book, you can continue to update the order book via Websocket incremental feed.
        If the difference between the end and start parameter is more than 500, please stop using this request and we suggest you to rebuild the Level 2 orderbook.

        Level 2 message pulling method: Take price as the key value and overwrite the local order quantity with the quantity in messages.
        If the quantity of a certain price in the pushed message is 0, please delete the corresponding data of that price.

        Param	Type	Description
        symbol	String	Symbol of the contract
        start	long	Start sequence number (included in the returned data)
        end	    long	End sequence number (included in the returned data)
        """

        params = {
            'symbol': symbol,
            'start' : start,
            'end'   : end
        }

        return self._request('GET', '/api/v1/level2/message/query', params)

    def get_l3_order_book(self, symbol):
        """
        Get a snapshot of all the open orders for a symbol. Level 3 order book includes all bids and asks (the data is non-aggregated, and each item means a single order).
        This API is generally used by professional traders because it uses more server resources and traffic, and we have strict access frequency control.

        To maintain up-to-date order book, please use Websocket incremental feed after retrieving the Level 3 snapshot.
        In the orderbook, the selling data is sorted low to high by price and orders with the same price are sorted in time sequence.
        The buying data is sorted high to low by price and orders with the same price are sorted in time sequence.
        The matching engine will match the orders according to the price and time sequence.
        The returned data is not sorted, you may sort the data yourselves.
        """

        params = {
            'symbol': symbol
        }

        return self._request('GET', '/api/v1/level3/snapshot', params)

    def get_l3_messages(self, symbol, start, end):
        """
        If the messages pushed by Websocket is not continuous, you can submit the following request and re-pull the data to ensure that the sequence is not missing.
        In the request, the start parameter is the sequence number of your last received message plus 1, and the end parameter is the sequence number of your current received message minus 1.
        After re-pulling the messages and applying them to your local exchange order book, you can continue to update the order book via Websocket incremental feed.
        If the difference between the end and start parameter is more than 500, please stop using this request and we suggest you to rebuild the Level 3 orderbook."""

        params = {
            'symbol': symbol,
            'start' : start,
            'end'   : end
        }

        return self._request('GET', '/api/v1/level3/message/query', params)

    def get_ticker(self, symbol):
        """
        The real-time ticker includes the last traded price, the last traded size, transaction ID, the side of liquidity taker, the best bid price and size, the best ask price and size as well as the transaction time of the orders.
        These messages can also be obtained through Websocket. The Sequence Number is used to judge whether the messages pushed by Websocket is continuous."""

        params = {
            'symbol': symbol
        }

        return self._request('GET', '/api/v1/ticker', params)

    def get_contracts_list(self):
        """
        Submit request to get the info of all open contracts."""

        return self._request('GET', '/api/v1/contracts/active')

    def get_contract_detail(self, symbol):
        """
        Submit request to get info of the specified contract."""

        params = {
            'symbol': symbol
        }

        return self._request('GET', '/api/v1/ticker', params)
