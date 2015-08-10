import os
from base64 import b16encode

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict

from .app import db


class Link(db.Model):
    id = db.Column(db.Unicode(), primary_key=True, nullable=False)
    dest = db.Column(db.Unicode(), nullable=False)
    created = db.Column(db.DateTime(), server_default=sa.text('NOW()'))
    deleted = db.Column(db.DateTime(), nullable=True)
    costum_tracking_variables = db.Column(
        MutableDict.as_mutable(HSTORE),
        nullable=False,
        server_default=sa.text("''::hstore")
    )


class Token(db.Model):
    token = db.Column(db.Unicode(), primary_key=True, nullable=False)
    created = db.Column(db.DateTime(), server_default=sa.text('NOW()'))
    deleted = db.Column(db.DateTime(), nullable=True)

    @classmethod
    def generate(cls):
        return cls(token=b16encode(os.urandom(16)).decode('us-ascii'))
