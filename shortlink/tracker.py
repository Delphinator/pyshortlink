# -*- coding: utf-8 -*-

import datetime
import json
from collections import ChainMap
from urllib.parse import urlencode

import requests


class DummyTracker(object):
    def track_visit(self, url, redirected_to, remote_addr, referer, time=None):
        pass


def check_request(url, post_payload, expected_response=200):
    assert requests.post(url, data=post_payload).status_code == \
        expected_response


class PiwikTracker(DummyTracker):
    def __init__(self, piwik_url, piwik_site_id, piwik_token, queue):
        self.piwik_url, self.piwik_site_id, self.piwik_token = \
            piwik_url, piwik_site_id, piwik_token
        self.queue = queue

    def track_visit(self, url, redirected_to, remote_addr, referer=None,
                    time=None, language=None, user_agent=None,
                    costum_variables=None):
        if time is None:
            time = datetime.datetime.utcnow()
        if costum_variables is None:
            costum_variables = {}

        base_args = {
            'apiv': '1',
            'rec': '1',
            'idsite': self.piwik_site_id,
            'cip': remote_addr,
            'cdt': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        if language is not None:
            base_args['lang'] = language
        if user_agent is not None:
            base_args['ua'] = user_agent

        landing_visit = {
            "url": url,
            "_cvar": {},  # visit scope costum variables
            "new_visit": "1",  # force a new visit
        }
        if referer is not None:
            landing_view["referer"] = referer
        # piwik expects strings as keys starting with "1"
        for idx, n in enumerate(sorted(costum_variables)):
            landing_visit["_cvar"][str(idx)] = [
                n, costum_variables[n]
            ]
        redirect_visit = {
            "url": redirected_to,
            "link": redirected_to,  # makes this an outgoing link
        }

        self.queue.enqueue(
            check_request,
            url=self.piwik_url,
            post_payload=json.dumps({
                "requests": [
                    dict(ChainMap(landing_visit, base_args)),
                    dict(ChainMap(redirect_visit, base_args)),
                ],
                "token_auth": self.piwik_token
            })
        )
