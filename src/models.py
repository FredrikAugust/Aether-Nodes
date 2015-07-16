'''This is where I work with the ORM; peewee
Defining Entry, connecting to and working with db
'''

from peewee import (Model, DoesNotExist, PostgresqlDatabase, TextField,
                    BooleanField)
import os
import re

__author__ = 'Fredrik A. Madsen-Malmo'

FULL = os.environ.get('DATABASE_URL', 'error')

# Get db content

result = re.search(
            '''
            (?P<dbname>[\w]+)\:\/\/
            (?P<username>[\w]+)\:
            (?P<password>[\w\d]+)\@
            (?P<server>[\w\d\.\-]+):
            (?P<port>[\d]+)\/
            (?P<database>[\w\d]+)\n
            ''', FULL, re.VERBOSE | re.MULTILINE)

DATABASE = PostgresqlDatabase(result.group('database'),
                              host=result.group('server'),
                              port=result.group('port'),
                              user=result.group('username'),
                              password=result.group('password'))


# Models

class Entry(Model):
    '''This is an entry that stores a "user".
    Very simple model as you can see'''

    name = TextField(default='Anonymous')
    ip = TextField(unique=True)
    port = TextField()
    online = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('online',)


# Init

def initialize():
    '''Initialise the database.'''

    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()
