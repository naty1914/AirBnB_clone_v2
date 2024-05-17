#!/usr/bin/python3
""" A script that runs a flask web framework """
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """  prints Hello HBNB! """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """  prints HBNB """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def cIsFun(text):
    """ It display “C ” followed by the value of the text """
    replace_string = text.replace('_', ' ')
    return f'C {replace_string}'


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def pythonText(text='is cool'):
    """ It display “Python ”, followed by the value of the text """
    replace_string = text.replace('_', ' ')
    return f'Python {replace_string}'


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ It display “n is a number """
    return f'{n} is a number'


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """ It display a HTML page only if n is an integer"""
    return render_template('5-number.html', n=n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
