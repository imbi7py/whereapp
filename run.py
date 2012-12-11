#!/usr/bin/env python
import sys
from flask import Flask
from flask import render_template
app = Flask(__name__)
app.debug = True

@app.route('/')
def main_page():
    info = {}
    return render_template('index.html', info=info)

if __name__ == '__main__':
    sys.exit(app.run(host='0.0.0.0'))
