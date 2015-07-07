__author__ = 'Fredrik A. Madsen-Malmo'

import socket
from flask import Flask, flash, render_template, g

import models
import forms

DEBUG = False
PORT = port = int(os.environ.get('PORT', 33507))
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = os.environ.get('secret_key', 'error')

# Before and after request

@app.before_request
def before_request():
    """Connect to db before each req"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
	"""Close the db connection after each req"""
	g.db.close()

	return response

# Routes

@app.route('/')
def index():
	return render_template('index.html')

# Start app

if __name__ == '__main__':
    models.initialize()
    try:
        models.Entry.create(
        	
        )
    except Exception:
        pass

    app.run(debug=DEBUG, port=PORT, host=HOST)
