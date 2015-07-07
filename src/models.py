__author__ = 'Fredrik A. Madsen-Malmo'

import datetime

from peewee import *
import os
import re

full = os.environ.get('DATABASE_URL', 'error')

# regex <3
result = re.search('(?P<dbname>[\w]+)\:\/\/(?P<username>[\w]+)\:(?P<password>[\w\d]+)\@(?P<server>[\w\d\.\-]+):(?P<port>[\d]+)\/(?P<database>[\w\d]+)\n', full, re.VERBOSE)

DATABASE = PostgresqlDatabase(result.group('database'), host=result.group('server'), port=result.group('port'), user=result.group('username'), password=result.group('password'))

# Models

class Entry(Model):
	timestamp = DateTimeField(default=datetime.datetime.now)
	name = TextField(default='Anonymous')
	ip = TextField()
	online = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('online', '-datetime')

# Init

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Entry], safe=True)
	DATABASE.close()