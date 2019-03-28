#!/usr/bin/env python

import random
import sys
import time

from slackclient import SlackClient

api_token = open('/home/ahidalgo/development/pizzabot/api.token').read().strip()
sc = SlackClient(api_token)

sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='@everyone 30 minutes until midnight!', link_names='true')
time.sleep(1790)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='10')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='9')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='8')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='7')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='6')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='5')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='4')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='3')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='2')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='1')
time.sleep(1)
sc.api_call('chat.postMessage', as_user='true', channel='dogfood',
            text='@everyone :tada: HAPPY NEW YEAR! :tada:', link_names='true')
