import os

import yaml
import foursquare
from flask import Flask, render_template, request, redirect, jsonify
from dropbox import session, client
path = os.path.dirname(os.path.realpath(__file__))+'/config.yaml'
_config = yaml.safe_load(open(path))


app = Flask(__name__)

redirect_uri = (
    _config['flask']['base_url'] + _config['foursquare']['redirect_uri'])
foursqclient = foursquare.Foursquare(
    client_id=_config['foursquare']['client_id'],
    client_secret=_config['foursquare']['client_secret'],
    redirect_uri=redirect_uri)

# remove for prod
foursqclient.set_access_token(_config['foursquare']['access_token'])

dbox_session = session.DropboxSession(_config['dropbox']['app_key'],
                                      _config['dropbox']['app_secret'],
                                      _config['dropbox']['access_type'])
# remove for prod
dbox_session.set_token(_config['dropbox']['access_token_key'],
                       _config['dropbox']['access_token_secret'])


@app.route('/dropbox/auth')
def dropbox_auth():
    redirect_uri = (_config['flask']['base_url'] +
                    _config['dropbox']['redirect_uri'])
    url = dbox_session.build_authorize_url(
        dbox_session.obtain_request_token(),
        oauth_callback=redirect_uri)
    return redirect(url, 302)


@app.route(_config['dropbox']['redirect_uri'])
def dropbox_oath():
    access_token = dbox_session.obtain_access_token(dbox_session.request_token)
    dbox_session.set_token(access_token.key,
                           access_token.secret)
    return redirect(_config['flask']['base_url'], 302)


@app.route(_config['foursquare']['redirect_uri'])
def foursquare_oauth():
    access_token = foursqclient.oauth.get_token(request.args.get('code'))
    # db store foursq access token
    foursqclient.set_access_token(access_token)
    return redirect(_config['flask']['base_url'], 302)


@app.route('/foursquare/auth')
def foursquare_auth():
    auth_uri = foursqclient.oauth.auth_url()
    return redirect(auth_uri, 302)


@app.route('/current_location.json')
def current_location():
    checkin = foursqclient.users.checkins(
        params={'limit': 1}).get('checkins').get('items')[0]
    return jsonify(checkin)


@app.route('/')
def main_page():
    checkin = foursqclient.users.checkins(params={'limit': 1})
    checkin = checkin['checkins']['items'][0]
    dbox_client = client.DropboxClient(dbox_session)
    latest_photo = dbox_client.metadata('/.gitshots')['contents'][-2]
    latest_photo = dbox_client.media(latest_photo['path'])['url']
    return render_template('index.html',
                           checkin=checkin,
                           latest_photo=latest_photo)

if __name__ == '__main__':
    app.debug = _config['flask']['debug']
    app.run(host=_config['flask']['host'], port=_config['flask']['port'])
