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

import asyncio
import os

from polofutures import WsClient


# Account Keys
API_KEY = os.environ['PF_API_KEY']
SECRET = os.environ['PF_SECRET']
API_PASS = os.environ['PF_PASS']

SYMBOL = 'BTCUSDTPERP'


async def ws_stream():
    def on_message(msg):
        if msg['topic'] == f'/contract/instrument:{SYMBOL}':
            print(f'Get {SYMBOL} Index Price: {msg["data"]}')
        elif msg['topic'] == f'/contractMarket/execution:{SYMBOL}':
            print(f'Last Execution: {msg["data"]}')
        elif msg['topic'] == f'/contractMarket/level2:{SYMBOL}':
            print(f'Get {SYMBOL} Level 2 :{msg["data"]}')

    ws_client = WsClient(on_message, API_KEY, SECRET, API_PASS)

    await ws_client.connect()

    await ws_client.subscribe(f'/contract/instrument:{SYMBOL}')
    await ws_client.subscribe(f'/contractMarket/execution:{SYMBOL}')
    await ws_client.subscribe(f'/contractMarket/level2:{SYMBOL}')

    await asyncio.sleep(30)

    await ws_client.disconnect()


if __name__ == '__main__':
    asyncio.run(ws_stream())
