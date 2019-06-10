#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import urllib.request
import unittest # TODO use unittest

def test_get(path, expected):
	req =  urllib.request.Request('http://127.0.0.1:5000{0}'.format(path))
	result = urllib.request.urlopen(req).read()
	print(result)
	assert result == expected

def test_post(path, data, expected):
	req =  urllib.request.Request('http://127.0.0.1:5000{0}'.format(path), data=data, method='POST')
	result = urllib.request.urlopen(req).read()
	print(result)
	assert result == expected

test_get('/', b'&#128154; Flask is running')
test_get('/json-sender/1234', b'{"uid": 5351, "public": "here are some public infos"}')
test_post('/json-receiver/1234', b'{}', b'1234')
