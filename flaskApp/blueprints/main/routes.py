
from flask import render_template, request

from flaskApp.db.sqlite import query_db
from flaskApp.extensions.cache_ext import cache

from . import bp_main

# ################################################################################
# ROUTES 
# ################################################################################

@bp_main.route("/")
@cache.cached()
def index():

  # fetch stickies & latest articles from blog
  stickies = query_db('SELECT * FROM posts WHERE is_sticky == 1 ORDER BY updated_at DESC LIMIT 2')
  latests = query_db(f'SELECT * FROM posts  WHERE is_sticky == 0 ORDER BY id DESC LIMIT {4 if len(stickies) < 2 else 7}')
  
  # show consent
  show_cookie_consent = False if request.cookies.get('sippas_cookie_consent') else True

  # render view
  return render_template("main/index.html", latests=latests, stickies=stickies, show_cookie_consent=show_cookie_consent)

@bp_main.route("/services")
@cache.cached(timeout=60*60*24*30)
def services():
  
  # render view
  return render_template("main/services.html")