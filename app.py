import os

from flask import Flask
from flask import jsonify
from flask import abort
from flask import render_template

import requests

app = Flask(__name__, static_url_path='/static')
app.config.from_pyfile('local_settings.py')


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    if port == 5000:
        app.debug = True
    else:
        app.config['PREFERRED_URL_SCHEME'] = 'https'

    app.run(host='0.0.0.0', port=port)
