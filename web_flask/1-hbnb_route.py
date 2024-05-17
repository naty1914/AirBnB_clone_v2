#!/usr/bin/python3
""" A script that runs a flask web framework """
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """  prints Hello HBNB! """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """  prints HBNB """
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
