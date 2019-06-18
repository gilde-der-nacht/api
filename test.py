#!/usr/bin/env python3

# https://docs.python.org/3/library/urllib.request.html#module-urllib.request
# requests module: https://2.python-requests.org/en/master/

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


def delete(path):
    req = requests.delete('http://127.0.0.1:5000{0}'.format(path))
    return req.content, req.status_code


assert get('/') == (b'&#128154; Flask is running', status_codes.StatusCode.HTTP_200_OK)

# assert 'time' in json.loads(get('/status')) -> doesn't work for me -> Thomas now i cannot work anymore because get returns a tuple

new_resource_data = '''
    {
        "public_body": {"name": "Anmeldungen Rollenspieltage 2019"},
        "private_body": {"email": "mail@abc.ch"}
    }
'''

updated_resource_data = '''
    {
        "public_body": {"name": "Anmeldungen Rollenspieltage 2019 UPDATED"},
        "private_body": {"email": "mail@xyz.ch"}
    }
'''

# route '/resources'
# GET
assert get('/resources') == (b'check', status_codes.StatusCode.HTTP_200_OK)

# POST
new_resource = post('/resources', new_resource_data)
created_resource_uid = new_resource[0]

assert len(created_resource_uid) == 64
assert new_resource[1] == status_codes.StatusCode.HTTP_201_CREATED

# PUT
assert put('/resources', updated_resource_data)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# DELETE
assert delete('/resources')[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# route '/resources/<uid>'
# GET
get_existing_resource = get('/resources/{0}'.format(created_resource_uid))
assert get_existing_resource[0] == created_resource_uid
assert get_existing_resource[1] == {"name": "Anmeldungen Rollenspieltage 2019"}  # TODO decide for " or ', ' has the advantage that it interrupts less if HTML is written inside strings
assert get_existing_resource[2] == {"email": "mail@abc.ch"}
assert get_existing_resource[3] == status_codes.StatusCode.HTTP_200_OK

get_non_existing_resource = get('/resources/{0}'.format('not_a_correct_uid'))
assert get_non_existing_resource[2] == status_codes.StatusCode.HTTP_204_NO_CONTENT

# POST
assert post('/resources/{0}'.format(created_resource_uid), new_resource_data)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# PUT
assert put('/resources/{0}'.format(created_resource_uid), updated_resource_data)[1] == status_codes.StatusCode.HTTP_201_CREATED

# DELETE
assert delete('/resources/{0}'.format(created_resource_uid))[1] == status_codes.StatusCode.HTTP_201_CREATED

new_entry_data = {
    "public_body": {"events": ["Workshop: Unicorns in Gaming", "D&D: But with Lightsaber"]},
    "private_body": {"name": "Hans Muster", "email": "mail@abc.ch"}
}

updated_entry_data = {
    "public_body": {"events": ["Workshop: Unicorns in Gaming"]},
    "private_body": {"name": "Hans Muster-Update", "email": "mail@xyz.ch"}
}

# route '/resources/<uid>/entries'
# GET
assert get('/resources/{0}/entries'.format(created_resource_uid)) == (b'check', status_codes.StatusCode.HTTP_200_OK)

# POST TODO do this comments POST, PUT, DELETE, ... really add something useful? what about using unittest (https://docs.python.org/3/library/unittest.html) and give the class a name which describes what you want to do, get TestAllowedMethods
new_entry = post('/resources/{0}/entries'.format(created_resource_uid), new_entry_data)
created_entry_uid = new_entry[0]
assert len(created_entry_uid) == 64
assert new_entry[1] == status_codes.StatusCode.HTTP_201_CREATED

# PUT
assert put('/resources/{0}/entries'.format(created_resource_uid), updated_entry_data)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# DELETE
assert delete('/resources/{0}/entries'.format(created_resource_uid))[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED

# route '/resources/<uid>/entries/<uid>'
# GET
get_existing_entry = get('/resources/{0}/entries/{1}'.format(created_resource_uid, created_entry_uid))
assert get_existing_entry[0] == created_entry_uid
assert get_existing_entry[1] == {"events": ["Workshop: Unicorns in Gaming", "D&D: But with Lightsaber"]}
assert get_existing_entry[2] == {"name": "Hans Muster", "email": "mail@abc.ch"}
assert get_existing_entry[3] == status_codes.StatusCode.HTTP_200_OK

get_non_existing_entry = get('/resources/{0}/entries/{1}'.format(created_resource_uid, 'not_a_correct_uid'))
assert get_non_existing_entry[2] == status_codes.StatusCode.HTTP_204_NO_CONTENT

# POST
assert post('/resources/{0}/entries/{1}'.format(created_resource_uid, created_entry_uid), new_entry_data)[1] == status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED  # TODO does breaking the line here really makes the code more readable?

# PUT
assert put('/resources/{0}/entries/{1}'.format(created_resource_uid, created_entry_uid), updated_entry_data)[1] == status_codes.StatusCode.HTTP_201_CREATED

# DELETE
assert delete('/resources/{0}/entries/{1}'.format(created_resource_uid, created_entry_uid))[1] == status_codes.StatusCode.HTTP_201_CREATED

# TODO test invalid id
# TODO add api version to status, use semantic versioning
