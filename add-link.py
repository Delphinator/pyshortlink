import sys

import requests

if len(sys.argv) != 4:
    sys.stderr.write('Usage: add-link.py TOKEN LINK REDIRECT_TO\n')
    sys.exit(1)

token, link, redirect_to = sys.argv[1:]

resp = requests.post(
    link,
    data={
        'dest': redirect_to
    },
    headers={
        'X-Token': token
    }
)
if resp.status_code != 200:
    print("Something went wrong! Response from server:")
    print(resp)
    print(resp.content.decode("utf-8"))
    sys.exit(1)
else:
    print("ok")
