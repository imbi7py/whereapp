from flask import Flask, render_template, Response, request, redirect

import foursquare
import yaml

_config = yaml.safe_load(file('config.yaml'))


app = Flask(__name__)
app.config.from_object(__name__)

foursqclient = foursquare.Foursquare(
                client_id=_config['foursquare']['client_id'],
                client_secret=_config['foursquare']['client_secret'],
                redirect_uri=_config['flask']['base_url'] +
                             _config['foursquare']['redirect_uri'])


@app.route(_config['foursquare']['redirect_uri'])
def foursquare_oauth():
    access_token = foursqclient.oauth.get_token(request.args.get('code'))
    print access_token
    # db store foursq access token
    foursqclient.set_access_token(access_token)
    return redirect(_config['flask']['base_url'], 302)


@app.route('/foursquare/auth')
def foursquare_auth():
    return redirect(foursqclient.oauth.auth_url(), 302)


@app.route('/')
def main_page():
    info = foursqclient.users()
    return render_template('index.html', info=info)


if __name__ == '__main__':
    app.debug = _config['flask']['debug']
    app.run()
