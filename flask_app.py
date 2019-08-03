#!/usr/bin/env python3

"""
# Run

export FLASK_APP=flask_app.py
export FLASK_ENV=development
export OLYMP_USERNAME=gdn
export OLYMP_PASSWORD=gdn
flask run

or

OLYMP_USERNAME=gdn OLYMP_PASSWORD=gdn FLASK_ENV=development FLASK_APP=flask_app.py flask run

# Linux Setup

apt-get install python3-flask-mail

# This flask microservice accepts REST requests as follows

domain: api.gildedernacht.ch/v1/
  '/resources'                     -> interact with ALL the resources
  '/resources/{uid}'               -> interact with ONE resource
  '/resources/{uid}/entries'       -> interact with ALL entries of one resource
  '/resources/{uid}/entries/{uid}' -> interact with ONE entry

methods:
  GET    -> read all data (if not authenticated, only public data)
  POST   -> write new data
  PUT    -> write a copied entry which does update some data (doesn't override anything)
  DELETE -> write a copied entry with the status 'deleted' (doesn't override anything)

# storage

  there are two kinds of data
      resources   -> buckets for entries of the same kind, enriched with a attributes (e.g. email address)
      entries     -> saved data (eg. form data or registrations for events),
          two main data sets (JSON format):
              public  -> public data, everybody can read it
              private -> can only be accessed with authentication

"""

import datetime
import os
import requests
import functools
import flask_mail
import collections

from storage import storage
from flask import Flask, request, json, send_from_directory, Response, redirect


app = Flask(__name__)


# see https://pythonhosted.org/Flask-Mail/ for E-Mail configuration
app.config['MAIL_PORT'] = 2500  # mailslurper uses port 2500 as default
mail = flask_mail.Mail(app)
MAIL_SENDER = 'anyone@gdn.any'
MAIL_RECIPIENTS = ['a@gdn.any', 'b@gdn.any', 'c@gdn.any']
MAIL_SUBJECT_PREFIX = 'GdN Mail '
DISABLE_EMAIL = True


def mail_send(subject, body):
    if DISABLE_EMAIL:
        return
    msg = flask_mail.Message(subject=MAIL_SUBJECT_PREFIX + subject, body=body, sender=MAIL_SENDER, recipients=MAIL_RECIPIENTS)
    mail.send(msg)


def auth_is_valid():
    username = os.environ.get('OLYMP_USERNAME')
    password = os.environ.get('OLYMP_PASSWORD')
    return request.authorization and (request.authorization.username == username) and (request.authorization.password == password)


def auth_required(fun):
    """
    decorator checks/handles if a page/resource should require authentication
    """
    @functools.wraps(fun)
    def decorator(*args, **kwargs):
        if not auth_is_valid():
            return Response('Authentication Required', requests.codes.UNAUTHORIZED, {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
        return fun(*args, **kwargs)
    return decorator


# TODO maybe only add domain we want (e.g. rollenspieltage.ch, spieltage.ch/...)
def cors(fun):
    @functools.wraps(fun)
    def decorator(*args, **kwargs):
        response = fun(*args, **kwargs)
        return Response(*response, headers={'Access-Control-Allow-Origin': '*'})
    return decorator


@app.route('/')
@cors
def server_status():
    return 'Olymp is Up &#128154;', requests.codes.OK


# TODO according to the API description on top, there should be the API version in front of the URL?
# TODO make version without filtering, or add a parameter to enable/disable it??
# TODO add parameter to limit maximum number of rows?
@app.route('/resources/<resource_uid>/entries', methods=['GET'])
@cors
def entries_list(resource_uid):
    auth = auth_is_valid()
    all_raw_entries = storage.entries_list(resource_uid) # storage returns a list sorted by timestamp (this is important for the following loop)
    all_entries_filtered = collections.OrderedDict()
    for (resource_uid, entry_uid, timestamp, identification, public_body, private_body, url, user_agent) in all_raw_entries:
        entry = {
            'resourceUid': resource_uid,
            'entryUid': entry_uid,
            'timestamp': timestamp,
            'identification': identification if auth else '',
            'publicBody': json.loads(public_body),
            'privateBody': json.loads(private_body) if auth else {},
            'url': url if auth else '',
            'userAgent': user_agent if auth else '',
        }
        all_entries_filtered[identification] = entry # because, as mentioned, the list is ordered, only the newest entry, with the same identification, is stored
    return json.dumps(list(all_entries_filtered.values())), requests.codes.OK


@app.route('/resources/<resource_uid>/entries', methods=['POST'])
@cors
def entries_add(resource_uid):
    if len(request.data) > 100_000:
        return '', requests.codes.REQUEST_ENTITY_TOO_LARGE
    body = json.loads(request.data)
    identification = body['identification']
    public_body = json.dumps(body['publicBody'])
    private_body = json.dumps(body['privateBody'])
    url = request.url
    user_agent = request.headers.get('User-Agent')
    entry = {
        'resourceUid': resource_uid,
        'identification': identification,
        'publicBody': public_body,
        'privateBody': private_body,
        'url': url,
        'userAgent': user_agent,
    }
    mail_send('entries_add', json.dumps(entry))
    entry = storage.entries_add(resource_uid, identification, public_body, private_body, url, user_agent)
    entry_uid = entry.get('uid')
    return entry_uid, requests.codes.CREATED


# TODO other url?
@app.route('/form/<resource_uid>', methods=['POST'])
@cors
def form(resource_uid):
    if len(request.data) > 100_000:
        return '', requests.codes.REQUEST_ENTITY_TOO_LARGE
    PUBLIC_PREFIX = 'public-'
    PRIVATE_PREFIX = 'private-'
    public = {}
    private = {}
    for key, value in request.form.items():
        if key.startswith(PUBLIC_PREFIX):
            public[key[len(PUBLIC_PREFIX):]] = value
        elif key.startswith(PRIVATE_PREFIX):
            private[key[len(PRIVATE_PREFIX):]] = value
    identification = ''  # TODO
    public_body = json.dumps(public)
    private_body = json.dumps(private)
    url = request.url
    user_agent = request.headers.get('User-Agent')
    entry = storage.entries_add(resource_uid, identification, public_body, private_body, url, user_agent)
    # TODO send email?
    # TODO default?
    redirectUrl = request.form['_redirect']
    return redirect(redirectUrl)


@app.route('/admin')
@auth_required
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/olymp.js')
def js():
    return send_from_directory('static', 'olymp.js')


@app.route('/status')
@cors
def status():
    status = {
        'version': '0.0.0',
        'time': datetime.datetime.now().isoformat(),
    }
    return json.dumps(status), requests.codes.OK
