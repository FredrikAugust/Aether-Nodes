__author__ = 'Fredrik A. Madsen-Malmo'

from flask import Flask, flash, render_template, g

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
        target = models.Entry.get(models.Entry.id == ip)
    except Exception:
        return False

    # 2 cycles and 0 bytes sent
    result = os.popen('ping -c 2 -s 0 {}'.format(ip)).read()

    if not (result.contains('Unknown host') or result.conatins('timeout')):
        target.update(
            online=True
        ).execute()

        return True

# Routes

@app.route('/', methods=['POST', 'GET'])
def index():
    form = forms.EntryForm()
    stream = models.Entry.select()

    if form.validate_on_submit():
        try:
            models.Entry.create(
                name=form.name.data,
                ip=form.ip.data,
                port=form.port.data,
                online=is_online(form.ip.data))

        except Exception:
            pass
    
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
