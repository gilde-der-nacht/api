from flask import Flask, abort, request, redirect, url_for

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def hello():
    return "<form action='/' method='POST'>" \
        "  Input:<br>" \
        "  <input type='text' name='returnPOST' value='post-demo' />" \
        "  <br><br>" \
        "  <input type='submit' value='Submit' />" \
        "</form> "\
        "<form action='/' method='GET'>" \
        "  Input:<br>" \
        "  <input type='text' name='returnGET' value='get-demo' />" \
        "  <br><br>" \
        "  <input type='submit' value='Submit' />" \
        "</form> " +  \
        print_out()


def print_out():
    if request.method == 'GET' and request.args.get('returnGET') is not None:
        return "Here is your String via GET method " + request.args.get('returnGET')
    elif request.method == 'POST' and request.form['returnPOST'] is not None:
        return "Here is your String via POST method " + request.form['returnPOST']
    else:
        return ""


@app.route('/also-forbidden')
def also_forbidden():
    return redirect(url_for('forbidden'))


@app.route('/forbidden')
def forbidden():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return "huh" + str(error)
