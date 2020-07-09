
polo-futures
--------
--------

Python 3 Wrapper for Poloniex Futures Exchange

DISCLAIMER: 
```
USE AT YOUR OWN RISK. You should not use this code in production unless you fully understand its limitations. 
Even if you understand the code and its limitations, you may incur losses when using this code for trading. 
When used in combination with your own code, the combination may not function as intended, and as a result you may incur losses. 
Poloniex is not responsible for any losses you may incur when using this code.
```
Features
--------

- Support for REST and websocket endpoints
- Simple handling of authentication
- Response exception handling

Getting Started
--------

- Register an account with [Poloniex](<https://www.poloniex.com/signup>).
- [Enable Futures Trading](https://www.poloniex.com/futures) for your account.
- Generate an [API Key](<https://www.poloniex.com/settings/futures-api-keys>).
- Set environment variables that contain your API Key values: `PF_API_KEY`, `PF_SECRET`, and `PF_PASS`.
- [Get the source files](#source).
- [Run one of the sample scripts](#samples).

<a name="source"></a>Get the code files with git.

Clone the repo into the path you will be using
```bash
git clone https://github.com/poloniex/polo-futures-sdk-python
```

<a name="samples"></a>Samples of the wrappers' usage are found in `rest_sample.py` and `ws_sample.py`. These can be run directly from python.
With, 
```bash
python rest_sample.py
```
OR
```bash
python ws_sample.py
```

Code Samples
--------

REST API
--------

```python
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
```

Websockets
-----------


```python
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


if __name__ == "__main__":
    asyncio.run(ws_stream())
```
