__author__ = 'Fredrik A. Madsen-Malmo'

from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

import socket

from models import Entry

# Custom validators

def ip_exist(form, field):
	if Entry.select().where(Entry.ip == field.data).exists():
		raise ValidationError('That IP is already registered.')

def port_open(form, field):
	# Don't know what this does, but I got it from SE and it works.
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		result = sock.connect_ex((form.ip.data, field.data))
	except Exception:
		raise ValidationError('Invalid values.')

	if result == 0:  # That means it works for some reason
	   pass
	else:
	   raise ValidationError('Please open port {} on your router.'.format(field.data))

# Form for a new entry

class EntryForm(Form):
	name = StringField(
		'name',
		validators=[
			DataRequired()])

	ip = StringField(
		'IP',
		validators=[
			DataRequired(),
			ip_exist])

	port = StringField(
		'port',
		validators=[
			DataRequired(),
			port_open])
