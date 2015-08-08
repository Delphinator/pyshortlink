#!/usr/bin/env python3
"""
Adds a link to a (possibly remote) pyshortlink instance

Usage:
    add_link.py [options] <link> <redirect_to>
    add_link.py (-h|--help)

Options:
    --token=<token>   Use this token to authentificate

If no token is given, the contents of ~/.pyshortlink.token are used. If no such
file can be found, an error is printed.
"""

import os
import sys

import requests
from docopt import docopt

args = docopt(__doc__)
if any(args[option] in args for option in ['-h', '--help']):
    sys.exit(0)


# -----------------------------------------------------------------------------
# --- input validation / error handling
# -----------------------------------------------------------------------------

token = args['--token']
if token is None:
    try:
        token = open(os.path.expanduser('~/.pyshortlink.token')).read().strip()
    except IOError:
        print("Error: --token not given and could not read " +
              "~/.pyshortlink.token", file=sys.stderr)
        sys.exit(1)

try:
    redirect_to_status_code = requests.head(args['<redirect_to>']).status_code
except requests.exceptions.MissingSchema:
    print('Error: Missing schema in url {}'.format(
        args['<redirect_to>']
    ), file=sys.stderr)
    sys.exit(1)
if redirect_to_status_code != 200:
    print('Error: {} returns HTTP {}, expected 200'.format(
        args['<redirect_to>'], redirect_to_status_code
    ), file=sys.stderr)
    sys.exit(1)


# -----------------------------------------------------------------------------
# --- this is the actual request to pyshortlink
# -----------------------------------------------------------------------------

resp = requests.post(
    args['<link>'],
    data={
        'dest': args['<redirect_to>']
    },
    headers={
        'X-Token': token
    }
)
if resp.status_code != 200:
    print("Something went wrong! Response from server:", file=sys.stderr)
    print(repr(resp), file=sys.stderr)
    print(resp.content.decode("utf-8"), file=sys.stderr)
    sys.exit(1)
else:
    print("ok")
