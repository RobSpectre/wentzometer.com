import os

from flask import Flask
from flask import escape
from flask import jsonify
from flask import abort
from flask import render_template
from flask import request

from flask_httpauth import HTTPBasicAuth

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import requests

from clock import tweet_snap_count


app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')

app.snap_percentage_manual = 98.6

app.creds = {'user': app.config['WENTZOMETER_ADMIN_USER'],
             'password':
             generate_password_hash(app.config['WENTZOMETER_ADMIN_PASSWORD'])}

auth = HTTPBasicAuth()


@app.route('/')
def index():
    return render_template('chart.html')


@app.route('/snap_count', methods=['GET', 'POST'])
def snap_count():
    result = requests.get('https://api.lineups.com/nfl/'
                          'fetch/snaps/2021/QB?season_type=1')

    if result.status_code == 200:
        data = result.json()

        for player in data['data']:
            if player['full_name'] == "Carson Wentz":
                return jsonify({'snap_percentage':
                                player['season_snap_percent']})

    else:
        abort(500)


@app.route('/snap_count_manual')
def snap_count_manual():
    return jsonify({'snap_percentage': app.snap_percentage_manual})


@auth.verify_password
def verify_password(user, password):
    if user == app.creds['user'] and \
       check_password_hash(app.creds['password'], password):
        return user


@app.route('/mod', methods=['GET', 'POST'])
@auth.login_required
def moderation():
    if request.method == 'POST':
        app.snap_percentage_manual = \
            float(escape(request.form['snap_count']))

        tweet_snap_count(app.snap_percentage_manual)

        return jsonify({'snap_count_percentage': app.snap_percentage_manual})
    else:
        return render_template('mod.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    if port == 5000:
        app.debug = True
    else:
        app.config['PREFERRED_URL_SCHEME'] = 'https'

    app.run(host='0.0.0.0', port=port)
