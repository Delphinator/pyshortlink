import os

from redis import Redis

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from rq import Queue

app = Flask('shortlink')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://shortlink:shortlink@localhost/shortlink'
for k in ['PIWIK_SITE_ID', 'PIWIK_URL', 'PIWIK_TOKEN',
          'SQLALCHEMY_DATABASE_URI']:
    if k in os.environ:
        app.config[k] = os.environ[k]
db = SQLAlchemy(app)
queue = Queue(connection=Redis())
