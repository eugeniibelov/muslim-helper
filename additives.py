#!/usr/bin/env python3

import sqlite3
import os.path

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mh.db')

con = sqlite3.connect(DB)
cur = con.cursor()

#  file = open('111', 'r')
#  for l in file:
    #  if l == '\n':
        #  continue
    #  l = l.strip().split(';')
    #  if len(l) == 5:
        #  l.append('')
    #  try:
        #  cur.execute("insert into additives values(?, ?, ?, ?, ?, ?)", l)
    #  except:
        #  print(l)
        #  exit(-1)

#  con.commit()

print("Код или название добавки: ", end='')
query = input().title()

while query != '':
    os.system('clear')
    db_res = cur.execute("SELECT code, ru_title, hukm_od FROM additives WHERE code LIKE :query or ru_title LIKE :query", {'query': "%" + query + '%',})

    for res in db_res.fetchall():
        print(res)

    print("Код или название добавки: ", end='')
    query = input().title()

