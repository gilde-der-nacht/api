#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import json
import urllib.request
import unittest  # TODO use unittest


def get(path):
    req = urllib.request.Request('http://127.0.0.1:5000{0}'.format(path))
    result = urllib.request.urlopen(req).read()
    #print(result)
    return result


def post(path, data):
    req = urllib.request.Request('http://127.0.0.1:5000{0}'.format(path), data=data, method='POST')
    result = urllib.request.urlopen(req).read()
    #print(result)
    return result


assert get('/') == b'&#128154; Flask is running'

assert 'time' in json.loads(get('/status'))

assert post('/post-json-to-container/uid/0123456789012345678901234567890101234567890123456789012345678901', b'{"public": [1, 2, 3], "private": [4, 5, 6]}') == b''

get_json = json.loads(get('/get-json-from-container/uid/0123456789012345678901234567890101234567890123456789012345678901'))

assert len(get_json) > 0

for entry in get_json:
	assert 'timestamp' in entry
	assert 'public' in entry
	assert 'private' in entry
	assert 'entry_uid' in entry
	assert 'container_uid' in entry
