import os
import datetime
import time

from flaskApp import app
from flask import render_template, abort, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flaskApp.db.sqlite import get_db, query_db
from flaskApp.db.algolia import index
from flask_login import login_required, current_user
from flaskApp.extensions.cache_ext import cache
from flaskApp.utils.decorators import has_role

from . import bp_blog
from .models import Tags 
from .forms import *

TAGS = Tags().getList()
BLOG_PAGE_SIZE = 9
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
# SEARCH PAGE
# -----------------------------------------------------------------
@bp_blog.route("/search", methods=('get', 'post'))
def posts_search():

  # init form
  form = PostsSearchForm()

  # init vars
  posts = []
  results = False

  # on validate
  if form.validate_on_submit():

    # retrieve data from algolia
    posts = index.search(form.title.data, { "hitsPerPage" : 100 })["hits"]

    # set results flag
    results = True

  # render view
  return render_template("blog/posts_search.html", form=form, posts=posts, results=results)


# -----------------------------------------------------------------
# VIEW SINGLE POST
# -----------------------------------------------------------------

@bp_blog.route("/view/<int:id>")
@cache.cached(timeout=60*60*24*30)
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
@has_role(["author", "editor", "admin"])
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
@has_role(["author", "editor", "admin"])
def dashboard_next(id):

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE id < ? ORDER BY id DESC LIMIT {}'.format(DASHBOARD_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/dashboard.html", posts=posts)

@bp_blog.route("/dashboard/prev/offset/<int:id>")
@login_required
@has_role(["author", "editor", "admin"])
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
@has_role(["author", "editor", "admin"])
def create_post():

  # init form
  form = PostCreateForm()

  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data
     
    # prepare data
    now = datetime.datetime.now()
    date = "{}-{}-{} {}:{}:{}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
    title = form_data["title"]
    body = form_data["md"].read().decode("utf-8")
    tags = " ".join(form_data["tags"])
    is_sticky = form_data["is_sticky"]
    author = current_user.get_author()

    # prepare name for teaser image
    try: 
      teaser_filename = "{}/{}/{}/{}".format(
        now.year, now.month, "#", 
        secure_filename(form_data["teaser"].filename)
      )
    except: teaser_filename = None
    
    # write data to sqlite
    cur = get_db().cursor()
    cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?,?,?,?,?,?)", 
      [ title, body, teaser_filename, tags, is_sticky, author, date, date, date ])
    get_db().commit()

    # algolia
    indexed_data = [{ 
      "objectID": cur.lastrowid, 
      "title": title, 
      "body": body[0:1000],
      "created_at": date,
      "updated_at": date
    }]
    index.add_objects(indexed_data)

    # upload teaser image
    if teaser_filename:
      path = os.path.join(app.root_path, 'static', 'blog', str(now.year), str(now.month), str(cur.lastrowid))
      if not os.path.exists(path): os.makedirs(path)
      form_data["teaser"].save(os.path.join(path, secure_filename(form_data["teaser"].filename)))
    
    # flash
    flash("Articolo creato correttamente.", "primary")

    # redirect on success
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, tags = Tags().getList())

@bp_blog.route("/edit/<int:id>", methods=['get','post'])
@login_required
@has_role(["author", "editor", "admin"])
def edit_post(id):

  # fetch post to be edited
  post = query_db('SELECT * FROM posts WHERE id = ?', [id], True)

  # no post no party
  if post == None: return abort(404) 
  
  # init form
  data = {}
  data["title"] = post["title"]
  data["tags"] = post["tags"].split(" ")
  data["is_sticky"] = post["is_sticky"]
  form = PostUpdateForm(data=data)
  
  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data
       
    # prepare name for teaser image
    try: 
      prefix = "/".join(post["created_at"].split("-")[0:2]) + "/#/"
      teaser_filename = prefix + secure_filename(form_data["teaser"].filename)
    except: teaser_filename = None

     # upload teaser image
    if teaser_filename:
      path = os.path.join(
        app.root_path, 'static', 'blog', 
        post["created_at"].split("-")[0], post["created_at"].split("-")[1], str(id))
      if not os.path.exists(path): os.makedirs(path)
      form_data["teaser"].save(os.path.join(path, secure_filename(form_data["teaser"].filename)))
   
    # -----------------------------------------------------------------
    # update post in sqlite
    # -----------------------------------------------------------------
    
    # date 
    date = time.strftime('%Y-%m-%d %H:%M:%S')

    # prepare data
    props = []
    props.append(("updated_at", date))
    props.append(("title", form_data["title"]))
    props.append(("teaser", teaser_filename))
    props.append(("tags", " ".join(form_data["tags"])))
    props.append(("is_sticky", form_data["is_sticky"]))
    if form_data["md"]:
      body = form_data["md"].read().decode("utf-8")
      props.append(("body", body))
    else:
      body = post["body"]
      props.append(("body", body))

    # build field update
    update_fields = ", ".join([ "{}=?".format(field_label) for field_label, value in props if value != None ])
    params = [ value for _, value in props if value != None  ] + [id]

    # write data to sqlite
    cur = get_db().cursor()
    cur.execute("UPDATE posts SET {} WHERE id=?".format(update_fields), params)
    get_db().commit()

    # algolia
    indexed_data = [{ 
      "objectID": id, 
      "title": form_data["title"], 
      "body": body[0:1000],
      "created_at": post["created_at"],
      "updated_at": date
    }]
    index.save_objects(indexed_data)

    # flash
    flash("L'articolo è stato creato correttamente", "primary")

    # redirect on success
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, post = post, tags = Tags().getList())

@bp_blog.route("/delete/<int:id>", methods=['post'])
@login_required
@has_role(["author", "editor", "admin"])
def delete_post(id):
  
  # delete post
  cur = get_db().cursor()
  cur.execute("DELETE FROM posts WHERE id=?", [id])
  get_db().commit()

  # algolia
  index.delete_objects([id])

  # flash
  flash("L'articolo è stato cancellato correttamente", "primary")

  # redirect
  return redirect(url_for('blog.dashboard'))

@bp_blog.route("/stickies/reset")
@login_required
@has_role(["author", "editor", "admin"])
def reset_stickies():
  
  # delete post
  get_db().execute("UPDATE posts SET is_sticky = 0")
  get_db().commit()

  # flash
  flash("L'operazione si è conclusa con successo", "primary")

  # redirect
  return redirect(url_for('blog.dashboard'))