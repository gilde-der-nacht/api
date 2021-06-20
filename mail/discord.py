#!/usr/bin/env python3

import requests

def msg_send(resource_uid, entry, msg, redirect_url, webhook):
    entry_url = 'https://api.gildedernacht.ch/resources/' + \
        resource_uid + '/entries/' + entry['uid']

    words = msg.split(' ')
    msg_excerpt = words if len(words) < 20 else words[0:10] + ['[...]'] + words[-10:]

    payload = {'content': 'Neue Nachricht von \'' + redirect_url + '\':'\
        '\n\n' \
        'Nachrichtauszug:\n' \
        '_' + (' '.join(msg_excerpt)) + '_' \
        '\n\n' + entry_url
    }

    requests.post(webhook, json=payload)
