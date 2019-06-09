from flask import Flask
from flask import request
app = Flask(__name__)


@app.route("/")
def hello():
    return "<form action='/new/' method='POST'>" \
        "  Input:<br>" \
        "  <input type='text' name='returnPOST' value='post-demo' />" \
        "  <br><br>" \
        "  <input type='submit' value='Submit' />" \
        "</form> "\
        "<form action='/new/' method='GET'>" \
        "  Input:<br>" \
        "  <input type='text' name='returnGET' value='get-demo' />" \
        "  <br><br>" \
        "  <input type='submit' value='Submit' />" \
        "</form> "


@app.route("/new/", methods=['POST', 'GET'])
def print_out():
    if request.method == 'POST':
        return "Here is your String via POST method " + request.form['returnPOST']
    else:
        return "Here is your String via GET method " + request.args.get('returnGET')
