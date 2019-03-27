import os
import time  

from flaskApp import app
from flask import render_template, abort, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flaskApp.db.sqlite import get_db, query_db
from flask_login import login_required, current_user
from flaskApp.extensions.cache_ext import cache

from . import bp_blog
from .models import Tags 
from .forms import *

TAGS = Tags().getList()
BLOG_PAGE_SIZE = 10
DASHBOARD_PAGE_SIZE = 25

# ################################################################################
# ROUTES FOR ALL
# ################################################################################

# -----------------------------------------------------------------
# LIST POSTS PER PAGE
# -----------------------------------------------------------------

@bp_blog.route("/")
@cache.cached()
def posts():
  
  # fetch posts
  posts = query_db('SELECT * FROM posts ORDER BY id DESC LIMIT {}'.format(BLOG_PAGE_SIZE))

  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts, 
    tags=TAGS, 
    pagination="blog/posts_pagination.html"
  )

@bp_blog.route("/next/offset/<int:id>")
@cache.cached()
def posts_next(id):
  
  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE id < ? ORDER BY id DESC LIMIT {}'.format(BLOG_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog.posts'))

  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts, 
    tags=TAGS, 
    pagination="blog/posts_pagination.html"
  )

@bp_blog.route("/prev/offset/<int:id>")
@cache.cached()
def posts_prev(id):
  
  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE id > ? ORDER BY id ASC LIMIT {}'.format(BLOG_PAGE_SIZE), [id])
  
  # no post no party
  if posts == []: return redirect(url_for('blog.posts'))

  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts[::-1], 
    tags=TAGS, 
    pagination="blog/posts_pagination.html"
  )

# -----------------------------------------------------------------
# LIST POSTS PER PAGE AND TAG
# -----------------------------------------------------------------

@bp_blog.route("/tag/<string:tag>")
@cache.cached()
def posts_tagged(tag):

  # no proper tag no party
  if tag not in TAGS: return redirect(url_for('blog.posts'))

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE tags LIKE "%{}%" ORDER BY id DESC LIMIT {}'.format(tag, BLOG_PAGE_SIZE))
  
  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts, 
    tag=tag, 
    tags=TAGS, 
    pagination="blog/posts_pagination_tagged.html"
  )

@bp_blog.route("/tag/<string:tag>/next/offset/<int:id>")
@cache.cached()
def posts_tagged_next(tag, id):

  # no proper tag no party
  if tag not in TAGS: return redirect(url_for('blog.posts'))
  
  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE tags LIKE "%{}%" AND id < ? ORDER BY id DESC LIMIT {}'.format(tag, BLOG_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog.posts_tagged', tag=tag))

  # render view
  return render_template(
    "blog/posts.html",  
    posts=posts, 
    tag=tag, 
    tags=TAGS,
    pagination="blog/posts_pagination_tagged.html"
  )

@bp_blog.route("/tag/<string:tag>/prev/offset/<int:id>")
@cache.cached()
def posts_tagged_prev(tag, id):

  # no proper tag no party
  if tag not in TAGS: return redirect(url_for('blog.posts'))

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE tags LIKE "%{}%" AND id > ? ORDER BY id ASC LIMIT {}'.format(tag, BLOG_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog.posts_tagged', tag=tag))
  
  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts[::-1], 
    tag=tag, tags=TAGS,
    pagination="blog/posts_pagination_tagged.html"
  )

# -----------------------------------------------------------------
# VIEW SINGLE POST
# -----------------------------------------------------------------

@bp_blog.route("/view/<int:id>")
@cache.cached()
def view_post(id):

  # fetch post
  post = query_db('SELECT * FROM posts WHERE id = ?', [id], True)
  latests = query_db('SELECT * FROM posts ORDER BY id DESC LIMIT 5')

  # no post no party
  if post == None: abort(404) 

  # render view
  return render_template("blog/post_view.html",  post=post, latests=latests, show_edit=current_user.is_active)


# ################################################################################
# ROUTES FOR ADMINS
# ################################################################################

# -----------------------------------------------------------------
# LIST POSTS + STICKIES
# -----------------------------------------------------------------

@bp_blog.route("/dashboard")
@login_required
def dashboard():
  
  # fetch posts
  posts = query_db("SELECT * FROM posts ORDER BY id DESC LIMIT {}".format(DASHBOARD_PAGE_SIZE))
  
  # render view
  return render_template("blog/dashboard.html", posts=posts)

@bp_blog.route("/dashboard/sticky")
@login_required
def dashboard_sticky():
  
  # fetch posts
  posts = query_db("SELECT * FROM posts WHERE is_sticky = 1 ORDER BY id DESC LIMIT {}".format(DASHBOARD_PAGE_SIZE))
  
  # render view
  return render_template("blog/dashboard.html", posts=posts)

# -----------------------------------------------------------------
# LIST POSTS PER PAGE
# -----------------------------------------------------------------

@bp_blog.route("/dashboard/next/offset/<int:id>")
@login_required
def dashboard_next(id):

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE id < ? ORDER BY id DESC LIMIT {}'.format(DASHBOARD_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/dashboard.html", posts=posts)

@bp_blog.route("/dashboard/prev/offset/<int:id>")
@login_required
def dashboard_prev(id):

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE id > ? ORDER BY id ASC LIMIT {}'.format(DASHBOARD_PAGE_SIZE), [id])
  
  # no post no party
  if posts == []: return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/dashboard.html", posts=posts[::-1])

# -----------------------------------------------------------------
# CREATE/UPDATE/DELETE POSTS + RESET STICKIES
# -----------------------------------------------------------------

@bp_blog.route("/create", methods=['GET', 'POST'])
@login_required
def create_post():

  # init form
  form = PostCreateForm()

  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data
  
    # prepare name for teaser image
    try: teaser_filename = secure_filename(form_data["teaser"].filename)
    except: teaser_filename = None
    
    # prepare data for other props
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    title = form_data["title"]
    body = form_data["md"].read().decode("utf-8")
    tags = " ".join(form_data["tags"])
    is_sticky = form_data["is_sticky"]
    author_id = current_user.get_author_id()
    
    # write data to sqlite
    cur = get_db().cursor()
    cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?,?,?,?,?,?)", 
      [ title, body, teaser_filename, tags, is_sticky, author_id, now, now, now ])
    get_db().commit()

    # upload teaser image
    if teaser_filename:
      path = os.path.join(app.root_path, 'static', 'blog', str(cur.lastrowid))
      if not os.path.exists(path): os.makedirs(path)
      form_data["teaser"].save(os.path.join(path, teaser_filename))
    
    # flash
    flash("Articolo creato correttamente.", "primary")

    # redirect on success
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, tags = Tags().getList())

@bp_blog.route("/edit/<int:id>", methods=['get','post'])
@login_required
def edit_post(id):

  # fetch post to be edited
  post = query_db('SELECT * FROM posts WHERE id = ?', [id], True)

  # no post no party
  if post == None: return abort(404) 

  # prepare data to populate form with
  data = {}
  data["title"] = post["title"]
  data["tags"] = post["tags"].split(" ")
  data["is_sticky"] = post["is_sticky"]
  
  # init form
  form = PostUpdateForm( data = data )
  
  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data
       
    # prepare name for teaser image
    try: teaser_filename = secure_filename(form_data["teaser"].filename)
    except: teaser_filename = None
   
    # -----------------------------------------------------------------
    # update post in sqlite
    # -----------------------------------------------------------------

    # prepare data
    props = []
    props.append(("updated_at", time.strftime('%Y-%m-%d %H:%M:%S')))
    props.append(("title", form_data["title"]))
    props.append(("teaser", teaser_filename))
    props.append(("tags", " ".join(form_data["tags"])))
    props.append(("is_sticky", form_data["is_sticky"]))
    props.append(("author_id", current_user.get_author_id()))
    if form_data["md"] != None:
      props.append(("body", form_data["md"].read().decode("utf-8")))
  
    # build field update
    update_fields = ", ".join([ "{}=?".format(field_label) for field_label, value in props if value != None ])
    params = [ value for _, value in props if value != None  ] + [id]

    # write data to sqlite
    cur = get_db().cursor()
    cur.execute("UPDATE posts SET {} WHERE id=?".format(update_fields), params)
    get_db().commit()

    # upload teaser image
    if teaser_filename:
      path = os.path.join(app.root_path, 'static', 'blog', str(id))
      if not os.path.exists(path): os.makedirs(path)
      form_data["teaser"].save(os.path.join(path, teaser_filename))

    # flash
    flash("L'articolo è stato creato correttamente", "primary")

    # redirect on success
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, post = post, tags = Tags().getList())

@bp_blog.route("/delete/<int:id>", methods=['post'])
@login_required
def delete_post(id):
  
  # delete post
  get_db().execute("DELETE FROM posts WHERE id = ?", [id])
  get_db().commit()

  # flash
  flash("L'articolo è stato cancellato correttamente", "primary")

  # redirect
  return redirect(url_for('blog.dashboard'))

@bp_blog.route("/stickies/reset")
@login_required
def reset_stickies():
  
  # delete post
  get_db().execute("UPDATE posts SET is_sticky = 0")
  get_db().commit()

  # flash
  flash("L'operazione si è conclusa con successo", "primary")

  # redirect
  return redirect(url_for('blog.dashboard'))