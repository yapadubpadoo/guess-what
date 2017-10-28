from flask import Flask, redirect, url_for, session, request
import pprint
import json

SECRET_KEY = 'development key'
DEBUG = True
FACEBOOK_APP_ID = ''
FACEBOOK_APP_SECRET = ''


app = Flask(__name__)
app.debug = DEBUG
app.secret_key = "my-secret"


@app.route('/fb/get-updates', methods=['GET','POST'])
def fb_realtime_updates():
    if request.args.get('hub.verify_token', '') == 'guesswhat':
        return request.args.get('hub.challenge')
    else:
        updates = json.loads(request.data.decode('utf-8'))
        pprint.pprint(updates)
        # todo, fetch data here
    return "OK"

if __name__ == '__main__':
    app.run()
