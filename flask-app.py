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


# GET: get all resources    -> UID, public (description), private (email address)
# POST: add new resource    -> public (description), private (email address), only if authenticated
# PUT: not allowed
# DELETE: not allowed
# TODO comment partially repeats the code, is obvious from the following line, which methods are supported
# TODO /resources isnt working yet
@app.route('/resources', methods=['GET', 'POST'])
def resources():
    if request.method != 'GET' and request.method != 'POST':
        abort(requests.codes.METHOD_NOT_ALLOWED)

    if request.method == 'GET':
        return storage.read_test_resource('095da522f49aebbd35443fd2349d578a1aaf4a9ea05ae7d59383a5f416d4fd3b'), requests.codes.OK

    # TODO use an elif, if it was a GET it is impossible to be a POST
    if request.method == 'POST':
        # public_body = request.data.get('public_body')
        # private_body = request.data.get('private_body')
        data = request.data
        # return str(json.loads(request.get_json()))
        # storage.write(public_body, private_body)
        return 'b3e35dfa2cd27cd385f08c246b6d49cf2e991c894d96828ba355063e77723fc0', requests.codes.CREATED


# GET: get all entries of this resource -> UIDs, meta info, public_body, private_body
# POST: add new entry                   -> public_body, private_body
# PUT: not allowed
# DELETE: not allowed
@app.route('/resources/<resource_uid>/entries', methods=['GET', 'POST'])
def entries(resource_uid):
    if request.method != 'GET' and request.method != 'POST':
        abort(requests.codes.METHOD_NOT_ALLOWED)

    if request.method == 'GET':
        all_entries = storage.read(resource_uid)
        return all_entries, requests.codes.OK

    # TODO use an elif, if it was a GET it is impossible to be a POST
    if request.method == 'POST':
        body = json.loads(request.data)
        public_body = json.dumps(body['publicBody'])
        private_body = json.dumps(body['privateBody'])
        url = request.url
        user_agent = request.headers.get('User-Agent')

        entry = storage.write(resource_uid, public_body, private_body, url, user_agent)
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


# TODO add api version so clients can test for an API and there may also be backward compatbility for the future
@app.route('/status')
def status():
    return json.dumps({
        'version': '0.0.0',
        'time': datetime.datetime.now().isoformat(),
    })
