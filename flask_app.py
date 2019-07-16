#!/usr/bin/env python3

"""
# Run

export FLASK_APP=flask_app.py
export FLASK_ENV=development
flask run

or

FLASK_APP=flask_app.py FLASK_ENV=development flask run

# Linux Setup

apt-get install python3-flask-mail

# This flask microservice accepts REST requests as follows

domain: api.gildedernacht.ch/v1/
  '/resources'                     -> interact with ALL the resources
  '/resources/{uid}'               -> interact with ONE resource
  '/resources/{uid}/entries'       -> interact with ALL entries of one resource
  '/resources/{uid}/entries/{uid}' -> interact with ONE entry

methods:
  GET     -> read all data (if not authenticated, only public data)
  POST    -> write new data
  PUT     -> write a copied entry which does update some data (doesn't override anything)
  DELETE  -> write a copied entry with the status 'deleted' (doesn't override anything)

# storage

  there are two kinds of data
      resources   -> buckets for entries of the same kind, enriched with a email address
      entries     -> saved data (eg. form data or registrations for events),
          two main data sets (JSON format):
              public  -> public data, everybody can read
              private -> only access with authentication

"""

import datetime
from functools import wraps

import requests
from flask import Flask, request, json, send_from_directory, Response

from storage import storage

app = Flask(__name__)


def auth_is_valid():
    return request.authorization and (request.authorization.username == 'gdn') and (request.authorization.password == 'gdn')


def auth_required(fun):
    """
    decorator checks/handles if a page/resource should require authentication
    """
    @wraps(fun)
    def decorator(*args, **kwargs):
        if not auth_is_valid():
            return Response('Authentication Required', requests.codes.UNAUTHORIZED, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
        return fun(*args, **kwargs)
    return decorator


# TODO this is just a first proof of concept, maybe there is a simple/other way to do it
# TODO maybe only add domain we want (e.g. rollenspieltage.ch, spieltage.ch/...)
def cors(fun):
    @wraps(fun)
    def decorator(*args, **kwargs):
        response = fun(*args, **kwargs)
        return Response(*response, headers={'Access-Control-Allow-Origin': '*'})
    return decorator


@app.route('/')
def server_status():
    return '&#128154; Flask is running', requests.codes.OK


@app.route('/resources/<resource_uid>/entries', methods=['GET'])
def entries_get(resource_uid):
    auth = auth_is_valid()
    all_raw_entries = storage.entries_list(resource_uid)
    all_entries = []
    for (resource_uid, entry_uid, timestamp, public_body, private_body, url, user_agent) in all_raw_entries:
        all_entries += [{
            'resourceUid': resource_uid,
            'entryUid': entry_uid,
            'timestamp': timestamp,
            'publicBody': public_body,
            'privateBody': private_body if auth else {},
            'url': url if auth else '',
            'userAgent': user_agent if auth else '',
        }]
    return json.dumps(all_entries), requests.codes.OK


# POST: Example JSON
# {"publicBody": {"name": "Anmeldungen Rollenspieltage 2019"}, "privateBody": {"email": "mail@xyz.ch"}}
@app.route('/resources/<resource_uid>/entries', methods=['POST'])
def entries_post(resource_uid):
    body = json.loads(request.data)
    public_body = json.dumps(body['publicBody'])
    private_body = json.dumps(body['privateBody'])
    url = request.url
    user_agent = request.headers.get('User-Agent')

    # debugging
    if True:
        return {public_body, private_body, url, user_agent}, requests.codes.OK

    entry = storage.entries_add(resource_uid, public_body, private_body, url, user_agent)
    entry_uid = entry.get('uid')

    return entry_uid, requests.codes.CREATED


@app.route('/admin')
@auth_required
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/test')
@auth_required
def test():
    return send_from_directory('static', 'test.html')


# TODO use the name of the application here
@app.route('/app.js')
def js():
    return send_from_directory('static', 'app.js')


# TODO add api version so clients can test for an API and there may also be backward compatibility for the future
@app.route('/status')
@cors
def status():
    status = {
        'version': '0.0.0',
        'time': datetime.datetime.now().isoformat(),
    }
    return json.dumps(status), requests.codes.OK
