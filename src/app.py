__author__ = 'Fredrik A. Madsen-Malmo'

from flask import Flask, flash, render_template, g, redirect

import socket

import models
import forms

import os

DEBUG = True
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

# Other functions

@app.route('/online/<ip>', methods=['POST', 'GET'])
def is_online(ip):
    try:
        target = models.Entry.get(models.Entry.ip == ip)
    except Exception:
        return 'False'

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, int(target.port)))
    except Exception:
        return 'False'

    if result == 0:
        target.update(
            online=True
        ).execute()

        return 'True'
    else:
        return 'True'

# Routes

@app.route('/new', methods=['POST'])
def new():
    form = forms.EntryForm()

    if form.validate_on_submit():
        try:
            online_stat = is_online(form.ip.data)

            models.Entry.create(
                name=form.name.data.strip(),
                ip=form.ip.data.strip(),
                port=form.port.data.strip(),
                online=online_stat)

        except Exception:
            pass

    return redirect(url_for('index'))

@app.route('/')
def index():
    stream = models.Entry.select()
    form = forms.EntryForm()
    
    return render_template('index.html', form=form, stream=stream)

# Start app

if __name__ == '__main__':
    models.initialize()

    try:
        models.Entry.get(models.Entry.ip == '93.184.204.215')
    except Exception:
        models.Entry.create(
        name='fotoply',
        ip='93.184.204.215',
        port='7077')

    app.run(debug=DEBUG, port=PORT, host=HOST)
