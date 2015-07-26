# Usage

First of we need an authentification token to add any new links. Do this on your server in the directory you installed shortlink in:

```
. venv/bin/activate
python generate-token.py
```

This will print out a random string. To add a link just do a POST request to the url you want to use with the `X-Token` header set to the token we just got and the `url` form field to the URL you want to redirect to.

```
# using curl
curl --post -H "X-Token: $TOKEN" --form "dest=http://example.com/some/long/path?with=query&params=as&well=!" http://redirect.example.com/l/homepage
```

Also look in `add-link.py` for a version using the `requests` python module.

Now you can give `http://redirect.example.com/l/homepage` to everyone instead of the long and hard to remember `http://example.com/some/long/path?with=query&params=as&well=!`.

Added benefit: You can have multiple links point to the same URL to track visits you got via different means (a Facebook post and a newsletter for example) separately. You will see a pageview and an outgoing link in piwik.

# Installation

```
# Create virtual environment to install dependencies in
# Important: Use python3.4
virtualenv --python=python3.4 venv
# Activate virtual environment
. venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Set database credentials. These are the defaults:
export SQLALCHEMY_DATABASE_URL='postgres://shortlink:shortlink@localhost/shortlink
# Run migrations (will create necessary tables)
alembic upgrade
```

# Running

## Web application in development mode
```
# Set database credentials. These are the defaults:
export SQLALCHEMY_DATABASE_URL='postgres://shortlink:shortlink@localhost/shortlink

. venv/bin/activate
python run.py
```

*NEVER* run this on a production machine or on a port reachable from the internet. The error page contains a shell, which is basically remote code execution vulnerability.

## Web application in production mode

Use your favorite  WSGI server. The WSGI callable is at `shortlink:app`. For example using uwsgi:

```
# Setup piwik tracking config. Just don't set those if you don't want that feature
export PIWIK_SITE_ID=1
export PIWIK_URL=http://example.com/piwik.php
export PIWIK_TOKEN=1
# Set database credentials. These are the defaults:
export SQLALCHEMY_DATABASE_URL='postgres://shortlink:shortlink@localhost/shortlink

. venv/bin/activate
pip install uwsgi
uwsgi --wsgi shortlink:app --socket uwsgi.socket
```

Then nginx can proxy requests to it like this:

```
location / {
    uwsgi_pass unix://<WHEREEVER YOUR SOCKET IS>;
    include uwsgi_params;  # should come with your nginx package
    uwsgi_param HTTP_HOST $host;
    uwsgi_param HTTP_X_SCRIPT_NAME {{ path }}/;
    uwsgi_param HTTP_X_SCHEME $scheme;
    uwsgi_param HTTP_X_REMPTE_ADDR $remote_addr;
    client_max_body_size 64M;
    client_body_buffer_size 1M;
}
```

## Background worker (used for asynchronously tracking visits)

```
. venv/bin/activate
rqworker
```
