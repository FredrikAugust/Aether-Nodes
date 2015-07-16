'''This is the main file for the aether nodes project'''

from flask import Flask, flash, render_template, g
import socket
import os

import models
import forms

__author__ = 'Fredrik A. Madsen-Malmo'

DEBUG = False
PORT = int(os.environ.get('PORT', 33507))
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
    '''Gets a request for a user and returns if the user is online.
    Also set\'s the online status of the user in the db.'''

    try:
        target = models.Entry.get(models.Entry.ip == ip)
    except models.Entry.DoesNotExist:
        return 'False'

    try:
        if not target.online:
            socket.setdefaulttimeout(0.5)
        else:
            socket.setdefaulttimeout(1.0)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, int(target.port)))
    except (socket.error, socket.timeout):
        target.online = False
        target.save()

        return 'False'

    if result == 0:
        target.online = True
        target.save()

        return 'True'
    else:
        target.online = False
        target.save()

        return 'False'


# Routes

@app.route('/', methods=['POST', 'GET'])
def index():
    '''Get\'s users from the db and sorts by online status.
    If the new entry form is passed it will try to create
    an entry
    '''

    stream = models.Entry.select().order_by(-models.Entry.online)
    form = forms.EntryForm()

    if form.validate_on_submit():
        if len(form.name.data.strip()) == 0:
            models.Entry.create(
                ip=form.ip.data.strip(),
                port=form.port.data.strip(),
                online=True)
        else:
            models.Entry.create(
                name=form.name.data.strip(),
                ip=form.ip.data.strip(),
                port=form.port.data.strip(),
                online=True)

        flash('Entry created.', 'success')
    else:
        pass

    return render_template('index.html', form=form, stream=stream)

# Start app

if __name__ == '__main__':
    models.initialize()

    try:
        models.Entry.get(models.Entry.ip == '93.184.204.215')
    except models.Entry.DoesNotExist:
        models.Entry.create(
            name='fotoply',
            ip='93.184.204.215',
            port='7077')

    app.run(debug=DEBUG, port=PORT, host=HOST)
