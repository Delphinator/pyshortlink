import datetime

import requests

import sqlalchemy as sa
from flask import abort, redirect, request

from .app import app, db, queue
from .auth import requires_auth
from .model import Link


def do_tracking_api_requests(url, params):
    for param in params:
        resp = requests.get(url, param)
        assert resp.status_code == 204


def track_visit(dest, time):
    if any(k not in app.config
           for k in ['PIWIK_SITE_ID',
                     'PIWIK_URL',
                     'PIWIK_TOKEN']
           ):
        return
    args = {
        'apiv': '1',
        'rec': '1',
        'idsite': app.config['PIWIK_SITE_ID'],
        'cip': request.remote_addr,
        'cdt': time.strftime('%Y-%m-%d %H:%M:%S'),
        'send_image': '0',
        'token_auth': app.config['PIWIK_TOKEN']
    }

    for p, h in {'lang': 'Accept-Language', 'ua': 'User-Agent'}.items():
        if h in request.headers:
            args[p] = request.headers[h]

    args1 = dict(args)
    args1['url'] = request.url
    if 'Referer' in request.headers:
        args1['urlref'] = request.headers['Referer']
    args1['new_visit'] = '1'  # force a new visit

    args2 = dict(args)
    args2['url'] = dest
    args2['link'] = dest

    queue.enqueue(do_tracking_api_requests,
                  app.config['PIWIK_URL'],
                  params=[args1, args2])


@app.route('/l/<path:id>')
def link(id):
    try:
        link = Link.query.filter_by(id=id, deleted=None).one()
        track_visit(link.dest, datetime.datetime.utcnow())
        return redirect(link.dest)
    except sa.orm.exc.NoResultFound:
        return abort(404)


@app.route('/l/<path:id>', methods=['POST'])
@requires_auth
def create_link(id):
    if request.content_length is None or request.content_length > 1024:
        return abort(400)
    try:
        db.session.add(Link(id=id, dest=request.form['dest']))
        db.session.commit()
    except sa.exc.IntegrityError:
        db.session.rollback()
        try:
            link = Link.query.filter_by(id=id).one()
            if link.deleted is None:
                msg = 'This redirect is already used. It points to "{}".\n'
            else:
                msg = 'This redirect is deleted. It pointed to "{}".\n'
            return msg.format(link.dest), 400
        except sa.orm.exc.NoResultFound:
            raise
    return "Success\n"
