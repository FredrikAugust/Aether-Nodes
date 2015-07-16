'''This is where I create all the logic for the forms,
and the forms themselves
'''

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

import socket

from models import Entry

__author__ = 'Fredrik A. Madsen-Malmo'


# Custom validators

def ip_exist(form, field):
    '''Check if the IP entered already exists'''

    if Entry.select().where(Entry.ip == field.data).exists():
        raise ValidationError('That IP is already registered.')


def port_open(form, field):
    '''Checks if the port entered is actually open and can
    be reached.
    '''

    if len(field.data) > 0:
        try:
            socket.setdefaulttimeout(2.0)
            # Don't know what this does, but I got it from SE and it works.
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except (socket.error, socket.timeout):
            pass

        try:
            result = sock.connect_ex((field.data, int(form.port.data)))
        except Exception:
            raise ValidationError('Invalid values.')

        if result == 0:  # That means it works for some reason
            pass
        else:
            raise ValidationError('Could not connect to {} on port {}.'
                                  .format(field.data, form.port.data))


# Form for a new entry

class EntryForm(Form):
    name = StringField(
        'name')

    ip = StringField(
        'IP',
        validators=[
            DataRequired(),
            ip_exist,
            port_open])

    port = StringField(
        'port',
        validators=[
            DataRequired()])
