#!/usr/bin/env python3

# export FLASK_APP=flask-app.py
# export FLASK_ENV=development
# flask run

# This flask microservice accepts REST requests as follows:
#
# storage:
#   there are two kinds of data
#       resources   -> buckets for entries of the same kind, enriched with a email address
#       entries     -> saved data (eg. form data or registrations for events),
#           two main data sets (JSON format):
#               public  -> public data, everybody can read
#               private -> only access with authentication
#
# domain: api.gildedernacht.ch/v1/
#   '/resources'                     -> interact with ALL the resources
#   '/resources/{uid}'               -> interact with ONE resource
#   '/resources/{uid}/entries'       -> interact with ALL entries of one resource
#   '/resources/{uid}/entries/{uid}' -> interact with ONE entry
#
# methods:
#   GET     -> read all data (if not authenticated, only public data)
#   POST    -> write new data
#   PUT     -> write a copied entry which does update some data (doesn't override anything)
#   DELETE  -> write a copied entry with the status 'deleted' (doesn't override anything)

import datetime

import requests
from flask import Flask, request, abort, json, send_from_directory
from storage import storage

app = Flask(__name__)


@app.route('/')
def server_status():
    return '&#128154; Flask is running', requests.codes.OK


@app.route('/resources/<resource_uid>/entries', methods=['GET'])
def entries_get(resource_uid):
    all_raw_entries = storage.entries_list(resource_uid)
    all_entries = []
    for (resource_uid, entry_uid, timestamp, url, user_agent, public_body, private_body) in all_raw_entries:
        all_entries += [[resource_uid, entry_uid, timestamp, json.loads(public_body), json.loads(private_body), url, user_agent]]
    return json.dumps(all_entries), requests.codes.OK

# POST: Example JSON {"publicBody": {"name": "Anmeldungen Rollenspieltage 2019"}, "privateBody": {"email": "mail@xyz.ch"}}
@app.route('/resources/<resource_uid>/entries', methods=['POST'])
def entries_post(resource_uid):
    body = json.loads(request.data)
    public_body = json.dumps(body['publicBody'])
    private_body = json.dumps(body['privateBody'])
    url = request.url
    user_agent = request.headers.get('User-Agent')

    entry = storage.entries_add(resource_uid, public_body, private_body, url, user_agent) # TODO write/read have different order of parmeteres
    entry_uid = entry.get('uid')

    return entry_uid, requests.codes.CREATED


# TODO authentication
@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')


# TODO authentication
@app.route('/test')
def test():
    return send_from_directory('static', 'test.html')


# TODO use the name of the application here
@app.route('/app.js')
def js():
    return send_from_directory('static', 'app.js')


# TODO add api version so clients can test for an API and there may also be backward compatibility for the future
@app.route('/status')
def status():
    return json.dumps({
        'version': '0.0.0',
        'time': datetime.datetime.now().isoformat(),
    })
