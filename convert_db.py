#!/usr/bin/env python

import datetime
import pymysql

foodlist = ''
with open('foodlist', 'r') as f:
  foodlist = f.readlines()

db = pymysql.connect(host='localhost', user='pizzabot', db='pizzachat')
cursor = db.cursor()
for line in foodlist:
  date = line[3:27]
  date = datetime.datetime.strptime(date, '%a %b %d %H:%M:%S %Y')
  date = date.strftime('%Y-%m-%d %H:%M:%S')
  who = line[29:].partition(' had: ')[0]
  what = line[29:].partition(' had: ')[2].strip()
  query = 'INSERT INTO foodlist (date, who, what) VALUES (TIMESTAMP(%s), %s, %s)'
  cursor.execute(query, (date, who, what))
  db.commit()
db.close()
