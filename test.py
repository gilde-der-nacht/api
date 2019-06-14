#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request

import requests
from utility import status_codes
import unittest  # TODO use unittest


def get(path):
    req = requests.get('http://127.0.0.1:5000{0}'.format(path))
    return req.content, req.status_code


def post(path, data):
    req = requests.post('http://127.0.0.1:5000{0}'.format(path), data=data)
    return req.content, req.status_code


def put(path, data):
    req = requests.put('http://127.0.0.1:5000{0}'.format(path), data=data)
    return req.content, req.status_code


def delete(path, data):
    req = requests.delete('http://127.0.0.1:5000{0}'.format(path), data=data)
    return req.content, req.status_code


assert get('/') == (b'&#128154; Flask is running', status_codes.StatusCode.HTTP_200_OK)

# assert 'time' in json.loads(get('/status')) -> doesn't work for me

# route '/resources'
# GET
assert get('/resources') == (b'check', status_codes.StatusCode.HTTP_200_OK)

# POST
data_01 = '''
    {
        "public_body": {"name": "Anmeldungen Rollenspieltage 2019"},
        "private_body": {"email": "mail@xyz.ch"}
    }
'''
new_resource = post('/resources', data_01)
assert len(new_resource[0]) == 64
assert new_resource[1] == status_codes.StatusCode.HTTP_201_CREATED

# PUT
assert put('/resources', data_01)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# DELETE
assert delete('/resources', data_01)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED


# route '/resources/<uid>'
# GET
get_existing_resources = get('/resources/{0}'.format(new_resource[0]))

assert get_existing_resources[1] == status_codes.StatusCode.HTTP_200_OK



# assert post('/post-json-to-container/uid/0123456789012345678901234567890101234567890123456789012345678901',
#             b'{"public": [1, 2, 3], "private": [4, 5, 6]}') == b''
#
# get_json = json.loads(
#     get('/get-json-from-container/uid/0123456789012345678901234567890101234567890123456789012345678901'))
#
# assert len(get_json) > 0
#
# for entry in get_json:
#     assert 'timestamp' in entry
#     assert 'public' in entry
#     assert 'private' in entry
#     assert 'entry_uid' in entry
#     assert 'container_uid' in entry

# TODO test invalid id
# TODO add api version to status, use semantic versioning
