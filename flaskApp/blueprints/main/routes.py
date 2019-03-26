
from flask import render_template

from flaskApp.db.sqlite import query_db
from flaskApp.extensions.cache_ext import cache

from . import bp_main

@bp_main.route("/")
@cache.cached()
def index():

  # fetch latest articles from blog
  stickies = query_db('SELECT * FROM posts WHERE is_sticky == 1 ORDER BY id DESC LIMIT 2')
  latest = query_db('SELECT * FROM posts  WHERE is_sticky == 0 ORDER BY id DESC LIMIT {}'.format(4 if len(stickies) < 2 else 7))

  # render view
  return render_template("main/index.html", latests=latest, stickies=stickies )

@bp_main.route("/services")
@cache.cached()
def services():

  # render view
  return render_template("main/services.html")

@bp_main.route("/gild")
@cache.cached()
def gild():

  # render view
  return render_template("main/gild.html")