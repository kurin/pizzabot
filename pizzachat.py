#!/usr/bin/env python

import sys

from slackclient import SlackClient

api_token = open('/home/ahidalgo/development/pizzabot/api.token').read().strip()
sc = SlackClient(api_token)

sc.api_call('chat.postMessage', as_user='true', channel=sys.argv[2],
            text=sys.argv[1], link_names=1)
