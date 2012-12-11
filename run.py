#!/usr/bin/env python
import sys
from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    sys.exit(app.run(host='0.0.0.0'))
