import os

from redis import Redis

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from rq import Queue

from .tracker import DummyTracker, PiwikTracker

app = Flask('shortlink')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://shortlink:shortlink@localhost/shortlink'
for k in ['PIWIK_SITE_ID', 'PIWIK_URL', 'PIWIK_TOKEN',
          'SQLALCHEMY_DATABASE_URI']:
    if k in os.environ:
        app.config[k] = os.environ[k]
db = SQLAlchemy(app)
queue = Queue(connection=Redis())

if all(k in app.config for k in [
        'PIWIK_SITE_ID',
        'PIWIK_URL',
        'PIWIK_TOKEN']):
    tracker = PiwikTracker(
        piwik_site_id=app.config["PIWIK_SITE_ID"],
        piwik_url=app.config["PIWIK_URL"],
        piwik_token=app.config["PIWIK_TOKEN"],
        queue=queue
    )
else:
    print("reporting visits to piwik is disabled")
    print("set PIWIK_SITE_ID, PIWIK_URL and PIWIK_TOKEN to enable")
    tracker = DummyTracker()
