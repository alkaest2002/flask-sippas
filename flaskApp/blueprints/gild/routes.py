
from flask import render_template, redirect, url_for

from flaskApp.db.sqlite import query_db
from flaskApp.extensions.cache_ext import cache

from . import bp_gild

AFFILITAES_PAGE_SIZE = 22

# ################################################################################
# ROUTES 
# ################################################################################

@bp_gild.route("/affiliates")
@cache.cached()
def affiliates(timeout=60*60*24*30):

  # fetch affiliates
  affiliates = query_db('SELECT * FROM affiliates ORDER BY last_name LIMIT ?', [AFFILITAES_PAGE_SIZE])
  
  # render view
  return render_template("gild/index.html", affiliates=affiliates)

@bp_gild.route("/affiliates/prev/offset/<int:id>")
@cache.cached(timeout=60*60*24*30)
def affiliates_prev(id):

  # fetch paginated affiliates
  affiliates = query_db('SELECT * FROM affiliates WHERE id < ? ORDER BY last_name DESC LIMIT ?', [ id, AFFILITAES_PAGE_SIZE ])

  # no affiliates no party
  if affiliates == []: return redirect(url_for('gild.affiliates'))

  # render view
  return render_template(
    "gild/index.html", 
    affiliates=affiliates[::-1]
  )

@bp_gild.route("/affiliates/next/offset/<int:id>")
@cache.cached(timeout=60*60*24*30)
def affiliates_next(id):

  # fetch paginated affiliates
  affiliates = query_db('SELECT * FROM affiliates where id > ? ORDER BY last_name ASC LIMIT ?', [ id, AFFILITAES_PAGE_SIZE ])

   # no affiliates no party
  if affiliates == []: return redirect(url_for('gild.affiliates'))
  
  # render view
  return render_template(
    "gild/index.html", 
    affiliates=affiliates
  )