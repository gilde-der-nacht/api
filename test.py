#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import json
import urllib.request
import unittest  # TODO use unittest


def get(path):
    req = urllib.request.Request('http://127.0.0.1:5000{0}'.format(path))
    result = urllib.request.urlopen(req).read()
    print(result)
    return result


def post(path, data):
    req = urllib.request.Request('http://127.0.0.1:5000{0}'.format(path), data=data, method='POST')
    result = urllib.request.urlopen(req).read()
    print(result)
    return result


assert get('/') == b'&#128154; Flask is running'
assert get('/json-sender/1234') == b'{"uid": 5351, "public": "here are some public infos"}'
assert post('/json-receiver/1234', b'{}') == b'1234'
assert 'time' in json.loads(get('/status'))
