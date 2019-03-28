"""Pizzabot primary library."""

import basketball
import datetime
import glob
import os
import pymysql
import pyowm
import random
import re
import sys
import time
import urllib2

from collections import Counter, defaultdict
from dateutil.relativedelta import relativedelta
from frinkiac import make_meme
from slackclient import SlackClient


def SimpsonsPic(sc, event):
  """Display a frinkiac search result based upon a query."""
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text='Something is broken and @alex has not fixed it yet. Blame him.')
  return
  search_text = event['text'][10:]
  if search_text:
    meme_url = make_meme(search_text)
    sc.api_call('chat.postMessage', as_user='true',
                channel=event['channel'], text=meme_url)


def FoodCheckIn(sc, event):
  """Log a food checkin to the database."""
  channel = sc.api_call('channels.info', channel=event['channel'])
  food = event['text'][9:]
  if food:
    if 'pizza' in food:
      sc.api_call('reactions.add', as_user='true', channel=event['channel'],
                  timestamp=event['ts'], name='pizza')
    user = sc.api_call('users.info', user=event['user'])
    db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
    cursor = db.cursor()
    query = 'INSERT INTO foodlist (who, what) VALUES (%s, %s)'
    cursor.execute(query, (user['user']['name'], food.encode('utf-8')))
    db.commit()
    db.close()


def FoodList(sc, event):
  """Display the last X things consumed, optionally with a search term."""
  count = 5
  after_command = event['text'][9:].lower()
  if re.match('^[1-9] ', after_command) or re.match('^[1-9]$', after_command):
    count = int(after_command[0])
  elif after_command and not re.match('^ ', after_command):
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='Command needs to be !foodlist, !foodlist QUERY or '
                     '!foodlistX QUERY where X is a number from 1-9')
    return
  text = 'The last %s things consumed:' % count
  search_term = event['text'][10:].lower().strip()
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  if search_term:
    cursor.execute(FoodListQuery(search_term, count, 'date'),
                   ("%" + search_term + "%"))
  else:
    cursor.execute(FoodListQuery(search_term, count, 'date'))
  foodlist = cursor.fetchall()
  db.close()
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=text)
  for item in reversed(foodlist):
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='On %s, %s had: %s' % item)


def FoodListQuery(term, count, order):
  selector = ''
  base = 'SELECT * FROM foodlist %s'
  base += ' ORDER BY %s DESC' % order
  if count:
    base += ' LIMIT %s' % count
  if term:
    selector = 'WHERE what LIKE %s'
  return base % selector


def FoodStats(sc, event):
  """Display some basic food statistics."""
  search_term = event['text'][11:].lower().strip()
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  if search_term:
    cursor.execute(FoodListQuery(search_term, 0, 'who'),
                   ("%" + search_term + "%"))
  else:
    cursor.execute(FoodListQuery(search_term, 0, 'who'))
    search_term = 'total'
  results = cursor.fetchall()
  db.close()
  if len(results) == 0:
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='I cannot find any %s checkins!' % search_term)
    return
  if search_term == 'commander':
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='There can be no commander commander!')
    return
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=TotalCheckins(results, search_term))
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=TopCheckins(results, search_term))
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=TopMonth(results, search_term))


def LastYear(sc, event):
  """Display what a user ate on this day last year."""
  user = sc.api_call('users.info', user=event['user'])
  lastyear = datetime.datetime.now() + relativedelta(years=-1)
  lastyear = lastyear.strftime('%%%Y-%m-%d%%')
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  query = 'SELECT what FROM foodlist WHERE who=%s AND date LIKE %s'
  cursor.execute(query, (user['user']['name'], lastyear))
  results = cursor.fetchall()
  db.close()
  if len(results) == 0:
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='You didn\'t eat anything this day last year!')
    return
  else:
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='Things %s ate on this day last year:' % user['user']['name'])
    for result in results:
      sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                  text=result)


def TotalCheckins(results, search_term):
  """Return text for total checkins line."""
  return 'There have been %s %s checkins.' % (len(results), search_term)


def FoodRank(search_term):
  """Return the proper food rank for a search term."""
  return _ranks[search_term.lower()]


def TopCheckins(results, search_term):
  """Return text for top checkins lines."""
  top_five = Counter([row[1] for row in results]).most_common()[:5]
  if search_term == 'total':
    search_term = 'checkin'
  (commander, count) = top_five.pop(0)
  text = 'The %s %s is %s with %s checkins.\n' % (
      search_term.title(), FoodRank(search_term), commander, count)
  text += 'Other %s fans include: ' % search_term
  if len(top_five) > 1:
    for eater in top_five[:-1]:
      text += '%s with %s, ' % eater
    text += 'and %s with %s.'  % top_five[-1]
  elif len(top_five) == 1:
    text += '%s with %s.' % top_five[0]
  else:
    text += 'No one.'
  return text


def TopMonth(results, search_term):
  """Return the busiest month."""
  top_months = Counter([row[0].strftime("%B %Y") for row in results])
  (month, count) = top_months.most_common()[0]
  if search_term == 'total':
    search_term = 'checkins'
  text = 'The most popular month for %s was %s with %s.' % (search_term,
                                                            month, count)
  return text


def ShouldI(sc, event):
  """Send a supportive response to those in need."""
  options = ['Yes, you should!',
             'I think that would be best.',
             'Hrmm... yes!',
             'Signs point to yes!',
             'That\'s the best idea I\'ve ever heard!',
             'D\'uh! Of course!',
             'Wow! What a great idea!',
             'What an incredible idea! You\'re a genius!',
             'Yes, yes! A thousand times, yes!',
             'Of course you should!',
             'I\'ve never heard of a better idea!',
             'Why didn\'t I think of that? You\'re brilliant!']
  response = random.choice(options)
  sc.api_call('chat.postMessage', as_user='true',
              channel=event['channel'], text=response)


def FoodSuggest(sc, event):
  """Display a random food checkin."""
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  query = 'SELECT * FROM foodlist ORDER BY RAND() LIMIT 1'
  cursor.execute(query)
  suggestion = cursor.fetchall()
  db.close()
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text='On %s, %s had: %s' % suggestion[0])


def PartyCheckIn(sc, event):
  """Log someone drinking or smoking to the DB. Clears out >2h old entries."""
  now = datetime.datetime.now()
  vice = event['text'][:5].lower()
  user = sc.api_call('users.info', user=event['user'])
  user = user['user']['name']
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  cursor.execute('DELETE FROM party WHERE date < '
                 '(NOW() - INTERVAL 120 MINUTE) AND who="%s"' % user)
  cursor.execute('INSERT INTO party (who, vice) VALUES ("%s", "%s")' % (user, vice))
  db.commit()
  cursor.execute('SELECT who FROM party WHERE who="%s" AND vice="%s"' % (user, vice))
  status = cursor.fetchall()
  party_message = PartyMessage(user, vice, len(status))
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=party_message)
  db.close()


def PartyList(sc, event):
  """List anyone currently drinking or smoking. Clears out >2h old entries."""
  db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
  cursor = db.cursor()
  cursor.execute('DELETE FROM party WHERE date < '
                 '(NOW() - INTERVAL 120 MINUTE)')
  cursor.execute('SELECT DISTINCT who FROM party WHERE vice="!booz"')
  booze = cursor.fetchall()
  cursor.execute('SELECT DISTINCT who FROM party WHERE vice="!weed"')
  weed = cursor.fetchall()
  drinking, smoking = '', ''
  if len(booze) > 1:
    drinking = ', '.join(value[0] for value in booze)
  elif len(booze) == 1:
    drinking = booze[0]
  else:
    drinking = 'No one.'
  if len(weed) > 1:
    smoking = ', '.join(value[0] for value in weed)
  elif len(weed) == 1:
    smoking = weed[0]
  else:
    smoking = 'No one.'
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text='Currently drinking: %s' % drinking)
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text='Currently stoned: %s' % smoking)
  db.close()


def PartyMessage(user, vice, status_count):
  """Figures out what message to return during a party checkin."""
  statuses = {'!weed': {1: 'smoking', 2: 'buzzed',
                        3: 'stoned', 4: 'stoned as fuck'},
              '!booz': {1: 'drinking', 2: 'tipsy',
                        3: 'drunk', 4: 'drunk as fuck'}}
  if user == 'christian':
    return '%s is now blotto!' % user
  for count, message in statuses[vice].iteritems():
    if count == status_count or (count == 4 and status_count > 4):
      return '%s is now %s.' % (user, message)


def CoffeeCheckIn(sc, event):
  """Log someone drinking coffee."""
  # TODO(sometimesitsalex): This still relies on the flat file, since we're
  # writing to both it and the database. Update this to only use the DB.
  with open('coffeelist', 'a') as f:
    now = datetime.datetime.now()
    user = sc.api_call('users.info', user=event['user'])
    f.write('On %s, %s had some coffee.\n' % (now.ctime(),
                                              user['user']['name']))


def ShittyCaption(sc, event):
  """Display a random Shitty New Yorker Cartoon Captions entry."""
  request = urllib2.Request(
      'http://shittynewyorkercartooncaptions.tumblr.com/random')
  result = urllib2.urlopen(request)
  sc.api_call('chat.postMessage', as_user='true',
              channel=event['channel'], text=result.geturl())


def IceT(sc, event):
  """Display a random Ice-T SVU."""
  request = urllib2.Request(
      'http://icetsvu.tumblr.com/random')
  result = urllib2.urlopen(request)
  sc.api_call('chat.postMessage', as_user='true',
              channel=event['channel'], text=result.geturl())


def Pizzachat(sc, event):
  """Display a random pizzachat image."""
  images = glob.glob('/var/www/html/talkingpizza/*.jpg')
  image = random.choice(images)
  image_url = 'http://talking.pizza/%s' % os.path.basename(image)
  sc.api_call('chat.postMessage', as_user='true',
              channel=event['channel'], text=image_url)


def Weather(sc, event):
  """Grab weather from openweathermap.org."""
  weather_message = 'You need to tell me where.'
  query = event['text'][9:]
  if len(query) > 0:
    api_key = open('weather.key').read().strip()
    weather_message = GetWeather(query, api_key)
  sc.api_call('chat.postMessage', as_user='true',
              channel=event['channel'], text=weather_message)


def GetWeather(query, api_key):
  """Query the openweathermap api using pyowm."""
  try:
    owm = pyowm.OWM(api_key)
    observation = owm.weather_at_place(str(query))
    location = observation.get_location()
    weather = observation.get_weather()
    temp = weather.get_temperature('fahrenheit')
    status = CleanupWeatherStatus(weather.get_detailed_status())
    return 'It is %sF degrees with %s in %s right now.' % (int(temp['temp']),
                                                           status,
                                                           location.get_name())
  except:
    return 'I couldn\'t find any weather for %s. I am sorry.' % (query)


def CleanupWeatherStatus(status):
  """Cleanup meteorological phrasing to read more cleanly."""
  weather_rewrites = {
    'clear sky': 'clear skies',
    'few clouds': 'a few clouds',
    'broken clouds': 'overcast skies',
    'intensity ': '',
    'thunderstorm': 'thunderstorms',
    'shower rain': 'rain showers',
    'shower snow': 'snow showers',
    'drizzle rain': 'drizzle'}
  for original, replacement in weather_rewrites.iteritems():
    status = re.sub(original, replacement, status)
  return status


def RIPReaction(sc, event):
  """React to any RIP message."""
  sc.api_call('reactions.add', as_user='true', channel=event['channel'],
              timestamp=event['ts'], name='rip')


def OnPace(sc, event):
  """OnPace predictions for NBA and NCAA games."""
  msg = '`!onpace (nba|ncaa) TEAM1 SCORE TEAM2 SCORE (quarter|half) MM:SS`'
  parsed = basketball.parse_input(event['text'])
  if parsed:
    if parsed[1].lower() == 'nba':
      predict = basketball.NBABasketballPrediction(parsed)
    elif parsed[1].lower() == 'ncaa':
      predict = basketball.NCAABasketballPrediction(parsed)
    else:
      sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                  text='Whoa! I\'ve never heard of that league! Sounds cool!')
      return
    if predict.validate_time():
      scores = predict.return_score()
      sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                  text=scores)
    else:
      sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='Proper format is: %s' % msg)
  else:
    sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
                text='Proper format is: %s' % msg)


def BasketballSeason(sc, event):
  """Inform everyone when the next college basketball season starts."""
  now = datetime.datetime.now()
  delta = relativedelta(datetime.date(2019,11,10), now)
  message = ('The 2017-18 NCAA College Basketball season starts in '
             '%(months)d months, %(days)d days, %(hours)d hours, '
             '%(minutes)d minutes and %(seconds)d seconds.' % delta.__dict__)
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=message)


def Olympics(sc, event):
  """How long until the summer olympics?"""
  now = datetime.datetime.now()
  delta = relativedelta(datetime.datetime(2020,7,24,22,0), now)
  message = ''
  if delta.seconds < 0:
    message = ':tada: THE OLYMPICS ARE HERE! :tada:'
  else:
    message = ('The Tokyo 2020 Summer Olympics will begin in '
               '%(years)d years, %(months)d months, %(days)d days, '
               '%(hours)d hours, %(minutes)d minutes and %(seconds)d '
               'seconds.' % delta.__dict__)
  sc.api_call('chat.postMessage', as_user='true', channel=event['channel'],
              text=message)


_ranks = defaultdict(lambda: 'Commander')
_ranks['banana'] = 'Commanda'
_ranks['resident'] = 'President'
_ranks['fig'] = 'Whig'
_ranks['roast'] = 'Boast'
_ranks['twinkie'] = 'Winkie'
_ranks['jerky'] = 'Turkey'
_ranks['turkey'] = 'Consumer'
_ranks['gravy'] = 'Lady'
_ranks['pie'] = 'Guy'
_ranks['ham'] = 'Man'
_ranks['roll'] = 'Troll'
_ranks['crepe'] = 'Creep'
_ranks['bean'] = 'Fiend'
_ranks['wing'] = 'Ding'
_ranks['dinner'] = 'Winner'
_ranks['ramp'] = 'Champ'

