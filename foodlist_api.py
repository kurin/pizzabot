#!/usr/bin/env python

import pymysql
import re

from datetime import datetime
from flask import Flask
from flask import jsonify
from flask_restful import Api
from flask_cors import CORS
from flask_cors import cross_origin
from flask_restful import Resource
from flask_restful import request


app = Flask(__name__)
cors = CORS(app, resources={r'/foodlist-api': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

class Foodlist(Resource):

  def __init__(self):
    self.starttime = ''
    self.endtime = ''

  def _validate_time(self, time):
    numbers = re.compile('^[0-9]+$')
    return numbers.match(time)

  def _convert_time(self, time):
    time = datetime.fromtimestamp(float(time)).strftime('%Y-%m-%d %H:%M:%S')
    return time

  def _get_foodlist(self):
    db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
    cursor = db.cursor()
    cursor.execute('SET NAMES utf8')
    if self.starttime == '' and self.endtime == '':
      cursor.execute('SELECT * FROM foodlist;')
    if self.starttime != '' and self.endtime == '':
      starttime = self._convert_time(self.starttime)
      cursor.execute('SELECT * FROM foodlist WHERE date >= "%s"' % starttime)
    if self.starttime == '' and self.endtime != '':
      endtime = self._convert_time(self.endtime)
      cursor.execute('SELECT * FROM foodlist WHERE date <= "%s"' % endtime)
    if self.starttime != '' and self.endtime != '':
      starttime = self._convert_time(self.starttime)
      endtime = self._convert_time(self.endtime)
      cursor.execute('SELECT * FROM foodlist WHERE date >= "%s" AND date <= "%s"'
                     % (starttime, endtime))
    foodlist = cursor.fetchall() 
    db.close()
    return self._convert_foodlist(foodlist)

  def _convert_foodlist(self, foodlist):
    keys = ['date', 'who', 'what']
    return [dict(zip(keys,line)) for line in foodlist]

  @cross_origin(origin='*',headers=['Content-Type', 'Authorization'])
  def get(self):
    if 'starttime' in request.args:
      if self._validate_time(request.args['starttime']):
        self.starttime = request.args['starttime']
    if 'endtime' in request.args:
      if self._validate_time(request.args['endtime']):
        self.endtime = request.args['endtime']
    return jsonify(self._get_foodlist())

api.add_resource(Foodlist, '/foodlist-api')

if __name__ == '__main__':
  app.run()
