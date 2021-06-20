#!/usr/bin/env python3

import datetime
import os

import requests
import functools
import collections

from storage import storage
from mail import mailjet
from mail import discord
from flask import Flask, request, json, send_from_directory, Response, redirect

app = Flask(__name__)


def load_config():
    CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH = CONFIG_PATH + '/config.json'
    with open(FILE_PATH, 'r') as file:
        config = json.load(file)
        return config


config = load_config()
username = config['auth']['username']
password = config['auth']['password']


mailClient = mailjet.config(
    config['mailjet']['public_key'],
    config['mailjet']['private_key'],
    config['mailjet']['version']
)


def auth_is_valid():
    return request.authorization and (request.authorization.username == username) and (
        request.authorization.password == password)


def auth_required(fun):
    """
    decorator checks/handles if a page/resource should require authentication
    """

    @functools.wraps(fun)
    def decorator(*args, **kwargs):
        if not auth_is_valid():
            return Response('Authentication Required', requests.codes.UNAUTHORIZED,
                            {'WWW-Authenticate': 'Basic realm="Authentication Required"'})
        return fun(*args, **kwargs)

    return decorator


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/')
def server_status():
    return 'Olymp is Up &#128154;', requests.codes.OK


# TODO according to the API description on top, there should be the API version in front of the URL?
# TODO make version without filtering, or add a parameter to enable/disable it??
# TODO add parameter to limit maximum number of rows?
@app.route('/resources/<resource_uid>/entries', methods=['GET'])
def entries_list(resource_uid):
    auth = auth_is_valid()
    all_raw_entries = storage.entries_list(
        resource_uid)  # storage returns a list sorted by timestamp (this is important for the following loop)
    all_entries_filtered = collections.OrderedDict()
    for (
            resource_uid, entry_uid, timestamp, identification, public_body, private_body, url,
            user_agent) in all_raw_entries:
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
        all_entries_filtered[
            identification.lower()] = entry  # because, as mentioned, the list is ordered, only the newest entry, with the same identification, is stored
    return json.dumps(list(all_entries_filtered.values())), requests.codes.OK


@app.route('/resources/<resource_uid>/entries', methods=['POST'])
def entries_add(resource_uid):
    if len(request.data) > 100_000:
        return '', requests.codes.REQUEST_ENTITY_TOO_LARGE
    body = json.loads(request.data)
    identification = body['identification']
    public_body = json.dumps(body['publicBody'])
    private_body = json.dumps(body['privateBody'])
    url = request.url
    user_agent = request.headers.get('User-Agent')
    mail_send(resource_uid, identification, public_body,
              private_body, url, user_agent, 'entries_add')
    entry = storage.entries_add(
        resource_uid, identification, public_body, private_body, url, user_agent)
    entry_uid = entry.get('uid')
    return entry_uid, requests.codes.CREATED


@app.route('/resources/<resource_uid>/entries/<entry_uid>', methods=['GET'])
@auth_required
def get_entry(resource_uid, entry_uid):
    return json.dumps(storage.entries_get(resource_uid, entry_uid))


@app.route('/form/<resource_uid>', methods=['POST'])
def form(resource_uid):
    if len(request.data) > 100_000:
        return '', requests.codes.REQUEST_ENTITY_TOO_LARGE
    PUBLIC_PREFIX = 'public-'
    PRIVATE_PREFIX = 'private-'
    IDENDTIFICATION = 'identification'
    CAPTCHA_SUFFIX = 'captcha'
    public = {}
    private = {}
    identification = ''
    spam = False
    for key, value in request.form.items():
        if key.endswith(CAPTCHA_SUFFIX):
            spam = (value != '')
        elif key.startswith(PUBLIC_PREFIX):
            public[key[len(PUBLIC_PREFIX):]] = value
        elif key.startswith(PRIVATE_PREFIX):
            private[key[len(PRIVATE_PREFIX):]] = value
        elif key == IDENDTIFICATION:
            identification = value

    public_body = json.dumps(public)
    private_body = json.dumps(private)
    url = request.headers.get('Referer')
    user_agent = request.headers.get('User-Agent')
    redirect_url = request.form.get('redirect', url)

    if spam:
        return redirect(redirect_url + '?msg=spam')

    entry = storage.entries_add(
        resource_uid, identification, public_body, private_body, url, user_agent)

    config = load_config()

    if ('message' in private) and (len(private['message']) > 0):
        message = private['message']
        msg = f'\'{message}\''
    else:
        msg = 'Nachricht war leer.'

    if 'rollenspieltage.ch' in redirect_url:
        recipient = {
            'email': 'mail@rollenspieltage.ch',
            'name': 'Luzerner Rpllenspieltage'
        }
        template = 'rollenspieltage'
    elif 'spieltage.ch' in redirect_url:
        recipient = {
            'email': 'mail@spieltage.ch',
            'name': 'Luzerner Spieltage'
        }
        template = 'spieltage'
    else:
        recipient = {
            'email': 'mail@gildedernacht.ch',
            'name': 'Gilde der Nacht'
        }
        template = 'gilde'

    discord.msg_send(resource_uid, entry, msg, redirect_url, config['discord']['inbox-webhook'])
    mailjet.mail_send(mailClient, msg, {'email': private['email'], 'name': private['name']}, recipient, template)

    return redirect(redirect_url + '?msg=success')


@app.route('/admin')
@auth_required
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/olymp.js')
def js():
    return send_from_directory('static', 'olymp.js')


@app.route('/status')
def status():
    status = {
        'version': '1.0.1',
        'time': datetime.datetime.now().isoformat(),
    }
    return json.dumps(status), requests.codes.OK
