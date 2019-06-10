from flask import Flask, request, abort, json
app = Flask(__name__)


@app.route('/')
def server_status():
    return '&#128154; Flask is running'


@app.route('/json-receiver/<uid>', method=['POST'])
def json_receiver(uid):
    if request.method != 'POST':
        abort(405)

    received_json = request.form['json']

    try:
        json.loads(received_json)
    except ValueError:
        abort(400)

    return uid


@app.route('/json-sender/<uid>')
def json_sender(uid):
    json_as_string = '{'\
                     'uid: 5351,' \
                     'public: "here are some public infos" ' \
                     '}'
    return json.loads(json_as_string)


@app.route('/admin')
def admin():
    return 'I return a HTML file'
