import sqlite3
import click
import os.path
from contextlib import closing

from flask import current_app, g
from flask.cli import with_appcontext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "blog.sqlite")

def get_db():
 
  # attach db to global
  if "db" not in g:
    g.db = sqlite3.connect(
      db_path, 
      detect_types = sqlite3.PARSE_DECLTYPES,
      isolation_level = "DEFERRED"
    )
    g.db.cursor().execute("PRAGMA journal_mode=WAL")
    g.db.row_factory = sqlite3.Row
  
  # return db
  return g.db

def query_db(query, args=(), one = False):
  
  # query and close cursor
  with closing(get_db().cursor().execute(query, args)) as cur:
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def close_db(e=None):
  
  # close connection
  db = g.pop('db', None)
  if db is not None: 
    db.close()
