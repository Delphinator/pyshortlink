import datetime

import requests

import sqlalchemy as sa
from flask import abort, redirect, request

from .app import app, db, tracker
from .auth import requires_auth
from .model import Link


@app.route('/l/<path:id>')
def link(id):
    try:
        link = Link.query.filter_by(id=id, deleted=None).one()

        tracker.track_visit(
            url=request.url,
            redirected_to=link.dest,
            remote_addr=request.remote_addr,
            referer=request.headers.get('Referer', default=None),
            language=request.headers.get('Accept-Language', default=None),
            user_agent=request.headers.get('User-Agent', default=None),
            costum_variables=link.costum_tracking_variables,
        )
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
