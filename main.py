from flask import Flask, render_template, Response, request

import werkzeug.serving
import foursquare
import yaml

yaml.safe_load('config.yml')


app = Flask(__name__)
app.config.from_object(__name__)

foursqclient = foursquare.Foursquare(client_id=0,
                                     client_secret=0,
                                     redirect_uri=0)


@app.route('/oauth/foursquare/authorize')
def foursquare_oauth():
    access_token = foursqclient.oauth.get_token(request['code'])
    # db store foursq access token
    foursqclient.set_access_token(access_token)




@app.route('/')
def main_page():
    info = {}
    return render_template('index.html', info=info)





@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    app.port = 6020
    app.run()


if __name__ == '__main__':
    run_dev_server()
