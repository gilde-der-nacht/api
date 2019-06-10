
import datetime

from flask import Flask, request, abort, json, send_from_directory
app = Flask(__name__)


@app.route('/')
def server_status():
    return '&#128154; Flask is running'


@app.route('/json-receiver/<uid>', methods=['POST'])
def json_receiver(uid):
    if request.method != 'POST':
        abort(405)

    try:
        received_data = request.get_data()
        print(received_data)
        json.loads(received_data)
    except ValueError:
        abort(400)

    print(uid)
    return uid


@app.route('/json-sender/<uid>')
def json_sender(uid):

    json_as_string = '{' \
                         '"uid": 5351, ' \
                         '"public": "here are some public infos"' \
                     '}'

    try:
        json.loads(json_as_string)
    except ValueError:
        abort(400)

    print(uid)
    return json_as_string


@app.route('/admin')
def admin():
    return send_from_directory('static', 'admin.html')


@app.route('/status')
def status():
    return '{"time": "' + str(datetime.datetime.now()) + '"}'
