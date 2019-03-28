import base64
import random
import re
import requests
import textwrap
import urllib


FRINKIAC_URL = 'https://frinkiac.com'
USER_AGENT = 'PIZZABOT'


def make_meme(query):
  episode, timestamp = get_frame(query)
  if episode == None and timestamp == None:
    return 'Sorry. Couldn\'t find anything for %s.' % query
  caption = get_caption(episode, timestamp)
  return get_meme_url(episode, timestamp, caption)


def validate_season(results):
  season_re = re.compile('S0[1-8]')
  for result in results:
    if season_re.match(result['Episode']):
      return result
  return None


def get_frame(query):
  r = requests.get(get_search_url(query), headers={'User-Agent': USER_AGENT})
  if not r.ok:
    return (None, None)
  results = r.json()
  frame = validate_season(results)
  if frame:
    return (frame['Episode'], frame['Timestamp'])
  else:
    return (None, None)


def get_caption(episode, timestamp):
  r = requests.get(get_caption_url(episode, timestamp),
                   headers={'User-Agent': USER_AGENT})
  if not r.ok:
    return None
  try:
    result = r.json()
    text = '\n'.join([subtitle['Content'] for subtitle in result['Subtitles']])
    return textwrap.fill(text, width=24)
  except:
    return None


def get_search_url(query):
  return '%s/api/search?q=%s' % (FRINKIAC_URL, urllib.quote(query))


def get_caption_url(episode, timestamp):
  return '%s/api/caption?e=%s&t=%s' % (FRINKIAC_URL, episode, timestamp)


def get_meme_url(episode, timestamp, caption):
  if caption:
    caption = urllib.quote(base64.b64encode(caption.encode('utf-8')))
    return '%s/meme/%s/%s.jpg?b64lines=%s' % (FRINKIAC_URL, episode, timestamp, caption)
  else:
    return '%s/meme/%s/%s.jpg' % (FRINKIAC_URL, episode, timestamp)
