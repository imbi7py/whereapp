from flask import Flask, render_template, Response, request
import werkzeug.serving
import yaml

yaml.safe_load('config.yml')




app = Flask(__name__)

foursqclient = foursquare.Foursquare(client_id=os.getenv("foursqclientid"),
                               client_secret=os.getenv("foursqclientsecret"),
                               redirect_uri="http://where.ranman.org/auth")

auth_uri = client.oauth.auth_url()


@app.route('/callback')
def callback_url():
    request.args.get('code')


@app.route('/')
def main_page():
    info = {}
    return render_template('index.html', info=info)


def get4sqcheckin():
    pass


@werkzeug.serving.run_with_reloader
def run_dev_server():
    app.debug = True
    app.port = 6020
    app.run()


if __name__ == '__main__':
    run_dev_server()
