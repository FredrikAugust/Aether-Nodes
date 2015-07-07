__author__ = 'Fredrik A. Madsen-Malmo'

import datetime

from peewee import *
import os
import re

full = os.environ.get('DATABASE_URL', 'error')

# Get db content

result = re.search(
			'''
				(?P<dbname>[\w]+)\:\/\/
				(?P<username>[\w]+)\:
				(?P<password>[\w\d]+)\@
				(?P<server>[\w\d\.\-]+):
				(?P<port>[\d]+)\/
				(?P<database>[\w\d]+)\n
			''', 
			full, re.VERBOSE|re.MULTILINE)

DATABASE = PostgresqlDatabase(result.group('database'), 
				host=result.group('server'), 
				port=result.group('port'), 
				user=result.group('username'), 
				password=result.group('password'))

# Models

class Entry(Model):
	name = TextField(default='Anonymous')
	ip = TextField(unique=True)
	port = TextField()
	online = BooleanField(default=False)

	class Meta:
		database = DATABASE
		order_by = ('online',)

# Init

def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Entry], safe=True)
	DATABASE.close()