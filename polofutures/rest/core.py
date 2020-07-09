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

import json
import requests
import hmac
import hashlib
import base64
import time
from urllib.parse import urljoin


_default_base_url = 'https://futures-api.poloniex.com'


class SendRequest:
    def __init__(self, key=None, secret=None, passphrase=None, base_url=None, timeout=5):
        self._key = key
        self._secret = secret.encode('utf-8') if secret else None
        self._passphrase = passphrase

        self._base_url = base_url or _default_base_url
        self._timeout = timeout

    def __call__(self, method, path, params=None, auth=False):
        body = None

        if params:
            if method in ['GET', 'DELETE']:
                params = [f'{key}={value}' for key, value in params.items()]
                params = '&'.join(params)
                path += '?' + params
            else:
                body = json.dumps(params)

        headers = {
            'Content-Type': 'application/json'
        }

        if auth:
            now = int(time.time()) * 1000
            str_to_sign = str(now) + method + path + (body or '')
            signature = hmac.new(self._secret, str_to_sign.encode('utf-8'), hashlib.sha256)
            signature = signature.digest()
            signature = base64.b64encode(signature)

            headers.update({
                'PF-API-SIGN'      : signature,
                'PF-API-TIMESTAMP' : str(now),
                'PF-API-KEY'       : self._key,
                'PF-API-PASSPHRASE': self._passphrase
            })

        url = urljoin(self._base_url, path)

        response = requests.request(method, url, headers=headers, timeout=self._timeout, data=body)

        try:
            payload = response.json()
        except:
            if response.status_code != 200:
                response.raise_for_status()

            raise RuntimeError(response.text)

        if payload['code'] == '200000':
            return payload.get('data', None)

        raise RuntimeError(payload)
