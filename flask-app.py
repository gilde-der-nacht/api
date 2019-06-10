import datetime

from flask import Flask, request, abort, json, send_from_directory
import storage

app = Flask(__name__)


@app.route('/')
def server_status():
    return '&#128154; Flask is running'


@app.route('/post-json-to-container/id/<uid>', methods=['POST'])
def post_json_to_container(uid):
    if request.method != 'POST':
        abort(405)

    try:
        public_body = request.form['public']
        json.loads(public_body)

        private_body = request.form['private']
        json.loads(private_body)

    except ValueError:
        abort(400)

    storage.write(uid, public_body, private_body)
    return uid


@app.route('/get-json-from-container/id/<uid>')
def get_json_from_container(uid):
    container = storage.read(uid)

    container_list = []

    for row in container:
        container_list.append(
            """
                { 
                    "entry_uid": %s,
                    "public_body": %s,
                    "private_body": %s,
                    "timestamp": %s
                }            
            """ % (row[1], row[2], row[3], row[4])
        )

    json_output = '{ "container": %s, "data":' % container[0][0]
    json_output += ', '.join(container_list)
    json_output += '}'

    return json_output


@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/status')
def status():
    return '{"time": "' + str(datetime.datetime.now()) + '"}'
