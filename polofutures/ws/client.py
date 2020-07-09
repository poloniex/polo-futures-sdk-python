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
import ssl
import certifi
import asyncio
import json
from uuid import uuid4

import websockets

from polofutures.rest.core import SendRequest

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = True
ssl_context.load_default_certs()
ssl_context.load_verify_locations(os.path.relpath(certifi.where()))


class WsClient:
    def __init__(self, on_message, key=None, secret=None, passphrase=None, base_url=None):
        self._on_message = on_message

        self._request = SendRequest(key, secret, passphrase, base_url)
        self._private = key is not None

        self._websocket = None
        self._conn_task = None
        self._conn_event = None
        self._ping_task = None
        self._keep_alive = False

        self._topics = {}

    async def connect(self):
        if self._websocket is not None:
            raise RuntimeError('Already connected to websocket')

        self._conn_event = asyncio.Event()
        self._keep_alive = True
        self._conn_task = asyncio.create_task(self._connect())
        self._ping_task = asyncio.create_task(self._ping())

        try:
            await asyncio.wait_for(self._conn_event.wait(), timeout=60)
        except asyncio.TimeoutError:
            self._keep_alive = False

            await self._cancel_ping_task()
            await self._cancel_conn_task()
            self._conn_event = None

            raise RuntimeError('Failed to connect to websocket')

    async def disconnect(self):
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')

        self._keep_alive = False

        await self._cancel_ping_task()
        await self._cancel_conn_task()
        self._conn_event = None

        self._topics.clear()

    async def _cancel_conn_task(self):
        self._conn_task.cancel()

        try:
            await self._conn_task
        except asyncio.CancelledError:
            pass

        self._conn_task = None

    async def _cancel_ping_task(self):
        self._ping_task.cancel()

        try:
            await self._ping_task
        except asyncio.CancelledError:
            pass

        self._ping_task = None

    def _get_ws_url(self):
        path = '/api/v1/bullet-public'

        if self._private:
            path = '/api/v1/bullet-private'

        token = self._request('POST', path, auth=self._private)

        params = {
            'connectId': uuid4(),
            'token': token['token'],
            'acceptUserMessage': self._private
        }
        params = [f'{key}={value}' for key, value in params.items()]
        params = '&'.join(params)

        url = token['instanceServers'][0]['endpoint']
        url = f'{url}?{params}'

        return url

    async def _connect(self):
        while self._keep_alive:
            try:
                url = self._get_ws_url()
            except:
                await asyncio.sleep(1)
                continue

            try:
                async with websockets.connect(url, ssl=ssl_context) as socket:
                    self._websocket = socket
                    self._conn_event.set()

                    for topic, kwargs in self._topics.items():
                        await self.subscribe(topic, **kwargs)

                    while self._keep_alive:
                        try:
                            msg = await socket.recv()
                            msg = json.loads(msg)
                        except json.decoder.JSONDecodeError:
                            pass
                        else:
                            try:
                                self._on_message(msg)
                            except:
                                pass
            except:
                # sleep before reconnecting
                await asyncio.sleep(1)
                continue
            finally:
                self._websocket = None
                self._conn_event.clear()

    async def subscribe(self, topic, **kwargs):
        msg = {
            'id': str(uuid4()),
            'privateChannel': False,
            'response': True
        }
        msg.update(kwargs)
        msg.update({
            'type': 'subscribe',
            'topic': topic
        })

        await self._send_message(msg)

        self._topics[topic] = kwargs

    async def unsubscribe(self, topic, **kwargs):
        msg = {
            'id': str(uuid4()),
            'privateChannel': False,
            'response': True
        }
        msg.update(kwargs)
        msg.update({
            'type': 'unsubscribe',
            'topic': topic
        })

        await self._send_message(msg)

        if topic in self._topics:
            del self._topics[topic]

    async def _ping(self):
        while self._keep_alive:
            await self._conn_event.wait()

            msg = {
                'type': 'ping',
                'id': str(uuid4())
            }

            try:
                await asyncio.wait_for(self._send_message(msg), timeout=10)
            except:
                pass

            await asyncio.sleep(50)

    async def _send_message(self, msg):
        if self._websocket is None:
            raise RuntimeError('Not connected to websocket')

        msg = json.dumps(msg)

        await self._websocket.send(msg)