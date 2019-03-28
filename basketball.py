"""Library for performing NBA and NCAAM basketball score predictions."""

import re


class NBABasketballPrediction(object):

  def __init__(self, parsed):
    self.team_one_name = parsed[2]
    self.team_one_score = parsed[3]
    self.team_two_name = parsed[4]
    self.team_two_score = parsed[5]
    self.period = parsed[6]
    self.time_left = parsed[7]

  def _seconds_left(self):
    time_list = self.time_left.split(':')
    other_time_left = 2880 - int(self.period) * 720
    return int(time_list[0]) * 60 + int(time_list[1]) + other_time_left

  def _compute_score(self, scorestr):
    score = int(scorestr)
    seconds_left = int(self._seconds_left())
    if seconds_left == 2880:
      return (score + (score * seconds_left))
    else:
      return (score + (score * seconds_left) / (2880 - seconds_left))

  def validate_time(self):
    time_list = self.time_left.split(':')
    if len(time_list) != 2:
      return False
    if (int(time_list[0]) < 0) or (int(time_list[0]) > 12):
      return False
    if (int(time_list[0]) == 12) and (int(time_list[1]) != 0):
      return False
    if (int(time_list[1]) < 0) or (int(time_list[1]) > 59):
      return False
    return True

  def return_score(self):
    team_one_predicted = self._compute_score(self.team_one_score)
    team_two_predicted = self._compute_score(self.team_two_score)
    result = 'On pace for %s: %s - %s: %s' % (self.team_one_name,
                                              team_one_predicted,
                                              self.team_two_name,
                                              team_two_predicted)
    return result


class NCAABasketballPrediction(object):

  def __init__(self, parsed):
    self.team_one_name = parsed[2]
    self.team_one_score = parsed[3]
    self.team_two_name = parsed[4]
    self.team_two_score = parsed[5]
    self.period = parsed[6]
    self.time_left = parsed[7]

  def _seconds_left(self):
    time_list = self.time_left.split(':')
    if self.period == '1':
      return int(time_list[0]) * 60 + int(time_list[1]) + 1200
    if self.period == '2':
      return int(time_list[0]) * 60 + int(time_list[1])

  def _compute_score(self, scorestr):
    score = int(scorestr)
    seconds_left = int(self._seconds_left())
    return (score + (score * seconds_left) / (2400 - seconds_left))

  def validate_time(self):
    time_list = self.time_left.split(':')
    if len(time_list) != 2:
      return False
    if (int(time_list[0]) < 0) or (int(time_list[0]) > 20):
      return False
    if (int(time_list[1]) < 0) or (int(time_list[1]) > 59):
      return False
    return True

  def return_score(self):
    team_one_predicted = self._compute_score(self.team_one_score)
    team_two_predicted = self._compute_score(self.team_two_score)
    result = 'On pace for %s: %s - %s: %s' % (self.team_one_name,
                                              team_one_predicted,
                                              self.team_two_name,
                                              team_two_predicted)
    return result


def parse_input(input_string):
  """Check to see if the mention should be responded to."""
  try:
    parsed = input_string.split(' ')
    if len(parsed) != 8:
      return False
    if parsed[1].lower() == 'nba':
      if not parsed[6] in ('1', '2', '3', '4'):
        return False
    elif parsed[1].lower() == 'ncaa':
      if not parsed[6] in ('1', '2'):
        return False
    else:
      return False
    if (int(parsed[3]) < 0) or (int(parsed[5]) < 0):
      return False
    parsed[3] = grab_digits(parsed[3])
    parsed[5] = grab_digits(parsed[5])
    if not check_time(parsed[7]):
      return False
    parsed[7] = check_time(parsed[7])
    return parsed
  except Exception as e:
    return False


def grab_digits(value):
  """Parse out only digits from the score array elements."""
  digits = ''
  try:
    digits = re.search(r'\d+', value).group()
  except:
    return False
  return digits


def check_time(value):
  """Ensure time is in a valid format."""
  time_left = ''
  try:
    time_left = re.search(r'\d{1,2}\:\d.', value).group()
  except:
    return False
  return time_left
