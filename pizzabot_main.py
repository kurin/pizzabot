#!/usr/bin/env python
"""Runner for Pizzabot."""

import pizzabot
import sys

from slackclient import SlackClient


COMMANDS = {'!basketball': pizzabot.BasketballSeason,
            '!booze': pizzabot.PartyCheckIn,
            '!checkin ': pizzabot.FoodCheckIn,
            '!coffee': pizzabot.CoffeeCheckIn,
            '!foodlist': pizzabot.FoodList,
            '!foodstats': pizzabot.FoodStats,
            '!icet': pizzabot.IceT,
            '!lastyear': pizzabot.LastYear,
            '!onpace': pizzabot.OnPace,
            '!party': pizzabot.PartyList,
            '!olympics': pizzabot.Olympics,
            '!pizzachat': pizzabot.Pizzachat,
            '!shitty': pizzabot.ShittyCaption,
            '!shouldi': pizzabot.ShouldI,
            '!simpsons ': pizzabot.SimpsonsPic,
            '!suggest': pizzabot.FoodSuggest,
            '!weather': pizzabot.Weather,
            '!weed': pizzabot.PartyCheckIn,
            'rip ': pizzabot.RIPReaction}


# Hacks to make it easier to deal with utf8 input
reload(sys)
sys.setdefaultencoding('utf8')
api_token = open('api.token').read().strip()
sc = SlackClient(api_token)
while True:
  try:
    if sc.rtm_connect():
      while True:
        new_events = sc.rtm_read()
        for event in new_events:
          if 'text' in event:
            message = event['text'].lower()
            for command, function in COMMANDS.iteritems():
              if message.startswith(command):
                function(sc, event)
  except Exception as e:
    print e
