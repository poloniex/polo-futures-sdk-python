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


class UserClient:
    def __init__(self, key=None, secret=None, passphrase=None, base_url=None):
        self._request = SendRequest(key, secret, passphrase, base_url)

    def get_account_overview(self, **kwargs):
        """
        Get Account Overview

        Param   	Type	Description
        currency	String	[Optional] Currecny ,including XBT,USDT,Default XBT"""
        return self._request('GET', '/api/v1/account-overview', kwargs, True)

    def get_transaction_history(self, **kwargs):
        """
        If there are open positions, the status of the first page returned will be Pending, indicating the realised profit and loss in the current 8-hour settlement period.
        Please specify the minimum offset number of the current page into the offset field to turn the page.

        Param	    Type	Description
        startAt	    long	[Optional] Start time (milisecond)
        endAt	    long	[Optional] End time (milisecond)
        type	    String	[Optional] Type RealisedPNL-Realised profit and loss, Deposit-Deposit, Withdrawal-withdraw, Transferin-Transfer in, TransferOut-Transfer out
        offset	    long	[Optional] Start offset
        maxCount	long	[Optional] Displayed size per page. The default size is 50
        currency	String	[Optional] Currency of transaction history XBT or USDT"""

        return self._request('GET', '/api/v1/transaction-history', kwargs, True)
