# Do we need `#!/usr/bin/env python3` here as well?

# TODO add description of the core ideas

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
#   '/resources'                    -> interact with ALL the resources
#   '/resources/{uid}'              -> interact with ONE resource
#   '/resources/{uid}/entries'      -> interact with ALL entries of one resource
#   '/resource/{uid}/entries/{uid}' -> interact with ONE entry
#
# methods:
#   GET     -> read all data (if not authenticated, only public data)
#   POST    -> write new data
#   PUT     -> write a copied entry which does update some data (doesn't override anything)
#   DELETE  -> write a copied entry with the status 'deleted' (doesn't override anything)

import datetime

from flask import Flask, request, abort, json, send_from_directory
from utility import status_codes
from storage import storage

app = Flask(__name__)


@app.route('/')
def server_status():
    return '''&#128154; Flask is running'''


@app.route('/resources', methods=['GET', 'POST'])
# GET: get all resources    -> UID, public (description), private (email address)
# POST: add new resource    -> public (description), private (email address)
# PUT: not allowed
# DELETE: not allowed
def resources():
    if request.method != 'GET' and request.method != 'POST':
        abort(status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED)

    if request.method == 'GET':
        return "check"
        # all_resources = storage.read_all('resources')

    if request.method == 'POST':
        storage.write('resource')


@app.route('/post-json-to-container/uid/<uid>', methods=['POST'])
def post_json_to_container(uid):
    # naming, we do not return a container we actually return the entries, /container/.../<uid> may return some statistics about the container or nothing at all

    if request.method != 'POST':
        abort(status_codes.StatusCode.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        # you used a "form" here, but this measn we have to generate a form with JS and inside the test, maybe this is the better idea, but client/server need to be both updated then, we can avoid the dumps so it may be worth to investigate
        received_data = request.get_data()
        received_json = json.loads(received_data)

        public_body = json.dumps(received_json['public'])
        private_body = json.dumps(received_json['private'])

        storage.write(uid, public_body, private_body)

    except ValueError:
        abort(status_codes.StatusCode.HTTP_400_BAD_REQUEST)

    return '{}'


@app.route('/get-json-from-container/uid/<uid>')
def get_json_from_container(uid):
    # TODO exception handling?
    # TODO use ''.format or f''

    try:
        container = storage.read(uid)
    except ValueError:
        abort(status_codes.StatusCode.HTTP_400_BAD_REQUEST)

    container_list = []

    if False:
        for row in container:
            # I removed the logic to merge container, ... what if we later add another method to return all entries? maybe we like to use the same code to display then, but in this case we have to differentiate between two possible results
            container_list.append(
                """
                    {
                        "container_uid": "%s",
                        "entry_uid": "%s",
                        "public": "%s",
                        "private": "%s",
                        "timestamp": "%s"
                    }
                """ % (row[0], row[1], row[2], row[3], row[4])

            )
            print(row)

        json_output = '[' + ', '.join(container_list) + ']';

    # simpler?

    if False:
        def convert(entry):
            return '{{"container_uid": "{0}", "entry_uid": "{1}", "public": "{2}", "private": "{3}", "timestamp": "{4}"}}'.format(
                *entry)

        container_list = map(convert, container)
        json_output = '[' + ', '.join(container_list) + ']';

    # better? we do not assemble json ourself ...

    if True:
        def convert(entry):
            return {"container_uid": entry[0], "entry_uid": entry[1], "public": json.loads(entry[2]),
                    "private": json.loads(entry[3]), "timestamp": entry[4]}

        container_list = map(convert, container)
        json_output = json.dumps(list(container_list))

    return json_output


@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/status')
def status():
    return '{"time": "' + str(datetime.datetime.now()) + '"}'
