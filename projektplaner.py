#!/usr/bin/python

import sqlite3
import sys
import os
import prettytable
from prettytable import from_db_cursor
from datetime import date


def args():
 
 if "-a" in sys.argv:
  if len(sys.argv) != 5:
   print("-a <name> <hours> <priority>")
   sys.exit(0)
  gimme_input()

 if "-s" in sys.argv:
  setup()

 if "-p" in sys.argv:
  update_prio()
  show_db()

 if "-e" in sys.argv:
  if len(sys.argv) != 4:
   print("-e <number> <newtime>")
   sys.exit(0)
  edit_hours(sys.argv[2],sys.argv[3]) 

 if "-m" in sys.argv:
  if len(sys.argv) != 3:
   print("-m <number>")
   sys.exit(0)
  mark_as_done(sys.argv[2])

if len(sys.argv) == 1 or "-h" in sys.argv:
 print("usage: ", sys.argv[0])
 print("-s SET UP THE DATABASE")
 print("-p PRINT THE DATABASE")
 print("-a <name> <hours> <priority> ADD A NEW ENTRY")
 print("-e <number> <newtime> EDIT AN ENTRIES HOURS")
 print("-m <number> MARK AN ENTRY AS DONE")
 sys.exit(0)

today = date.today()
now = today.strftime("%Y-%m-%d")

dir = os.environ['HOME'] + "/projekte.db"

connect = sqlite3.connect(dir)
cursor = connect.cursor()
connect.row_factory = sqlite3.Row


def setup():
 cursor.execute("""CREATE TABLE projects
		(number integer, name text, hours integer, priority integer, status text, date text)
		""")
 connect.commit()
 sys.exit(0)


def show_db():
 cmd = "SELECT number, name, hours, priority, status FROM projects WHERE status = 'open' ORDER BY priority DESC"
 cursor.execute(cmd)
 pt = from_db_cursor(cursor)
 print(pt)


def gimme_input():
 newnumber = 1
 cursor.execute("SELECT number FROM projects")
 for line in cursor.fetchall():
  for element in line:
   newnumber = element + 1
 cursor.execute("INSERT INTO projects VALUES (?,?,?,?,?,?)",(newnumber,sys.argv[2],sys.argv[3],sys.argv[4],"open",now))
 connect.commit()

def edit_hours(number,newtime):
 cursor.execute("UPDATE projects SET hours =? WHERE number =?",(newtime,number))
 connect.commit()

def mark_as_done(number):
 cursor.execute("UPDATE projects SET status = 'done' WHERE number =?",[number])
 connect.commit()

def update_prio():
 cursor.execute("UPDATE projects SET priority = priority + 1 WHERE date <?",[now])
 cursor.execute("UPDATE projects SET date =?",[now])
 cursor.execute("UPDATE projects SET priority = 4 WHERE priority > 4")
 connect.commit()


args()
