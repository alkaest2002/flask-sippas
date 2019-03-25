import os
import mistune
import copy

from flask import render_template, abort, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flaskApp.db.sqlite import get_db, query_db
from flaskApp import app
from flask_login import login_required, current_user

from . import bp_blog
from .models import Tags 
from .forms import *

TAGS = Tags().getList()
BLOG_PAGE_SIZE = 8
DASHBOARD_PAGE_SIZE = 25

markdown = mistune.Markdown()

# ################################################################################
# ROUTES FOR ALL
# ################################################################################

# -----------------------------------------------------------------
# LIST POSTS PER PAGE
# -----------------------------------------------------------------

@bp_blog.route("/")
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
def posts_tagged(tag):

  # no proper tag no party
  if tag not in TAGS: return redirect(url_for('blog.posts'))

  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE tags LIKE "%{}%" ORDER BY id DESC LIMIT {}'.format(tag, BLOG_PAGE_SIZE))
  
  # no post no party
  if posts == []: return redirect(url_for('blog.posts'))

  # render view
  return render_template(
    "blog/posts.html", 
    posts=posts, 
    tag=tag, 
    tags=TAGS, 
    pagination="blog/posts_pagination_tagged.html"
  )

@bp_blog.route("/tag/<string:tag>/next/offset/<int:id>")
def posts_tagged_next(tag, id):

  # no proper tag no party
  if tag not in TAGS: return redirect(url_for('blog.posts'))
  
  # fetch posts
  posts = query_db('SELECT * FROM posts WHERE tags LIKE "%{}%" AND id < ? ORDER BY id DESC LIMIT {}'.format(tag, BLOG_PAGE_SIZE), [id])

  # no post no party
  if posts == []: return redirect(url_for('blog_tagged.posts', tag=tag))

  # render view
  return render_template(
    "blog/posts.html",  
    posts=posts, 
    tag=tag, 
    tags=TAGS,
    pagination="blog/posts_pagination_tagged.html"
  )

@bp_blog.route("/tag/<string:tag>/prev/offset/<int:id>")
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
def view_post(id):

  # fetch post
  post = query_db('SELECT * FROM posts WHERE id = ?', [id], True)

  # no post no party
  if post == None: abort(404) 

  # render view
  return render_template("blog/post_view.html",  post = post)


# ################################################################################
# ROUTES FOR ADMINS
# ################################################################################

@bp_blog.route("/dashboard")
@bp_blog.route("/dashboard/<int:is_sticky>")
@login_required
def dashboard(is_sticky = None):
  
  # fetch posts
  sql = "SELECT * FROM posts {} ORDER BY id DESC LIMIT {}"\
    .format('WHERE is_sticky = 1' if is_sticky == 1 else None, DASHBOARD_PAGE_SIZE)
  
  # render view
  return render_template("blog/dashboard.html", posts = query_db(sql))

@bp_blog.route("/create", methods=['GET', 'POST'])
@login_required
def create_post():

  # init form
  form = PostCreateForm()

  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data

    # -----------------------------------------------------------------
    # upload teaser image
    # -----------------------------------------------------------------
    
    # store teaser image
    teaser = form.teaser.data
    teaser_filename = None
    if teaser != None:
      teaser_filename = secure_filename(teaser.filename)
      teaser.save(os.path.join(app.root_path, 'static', 'blog', teaser_filename))

    # -----------------------------------------------------------------
    # write new post to sqlite
    # ----------------------------------------------------------------- 

    # prepare data
    title = form_data["title"]
    body = markdown(form_data["md"].read().decode("utf-8"))
    teaser = teaser_filename
    tags = " ".join(form_data["tags"])
    is_sticky = form_data["is_sticky"]
    author_id = current_user.get_author_id()
    
    # write
    get_db().execute("INSERT INTO posts VALUES(NULL,?,?,?,?,?,?)", [title, body, teaser, tags, is_sticky, author_id])
    get_db().commit()
    
    flash("Articolo creato correttamente", "primary")
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, tags = Tags().getList())

@bp_blog.route("/edit/<int:id>", methods=['get','post'])
@login_required
def edit_post(id):

  # fetch post
  post = query_db('SELECT * FROM posts WHERE id = ?', [id], True)

  # no post no party
  if post == None: return abort(404) 

  # init form
  data = {}
  data["title"] = post["title"]
  data["tags"] = post["tags"].split(" ")
  data["is_sticky"] = post["is_sticky"]
  form = PostUpdateForm( data = data )

  # on validate
  if form.validate_on_submit():

    # cache form data
    form_data = form.data
   
    # -----------------------------------------------------------------
    # upload teaser image
    # -----------------------------------------------------------------
    
    # store teaser image
    teaser = form.teaser.data
    teaser_filename = None
    if teaser != None:
      teaser_filename = secure_filename(teaser.filename)
      teaser.save(os.path.join(app.root_path, 'static', 'blog', teaser_filename))
   
    # -----------------------------------------------------------------
    # update post in sqlite
    # -----------------------------------------------------------------

    # prepare data
    props = []
    props.append(("title", form_data["title"]))
    props.append(("teaser", teaser_filename))
    props.append(("tags", " ".join(form_data["tags"])))
    props.append(("is_sticky", form_data["is_sticky"]))
    props.append(("author_id", current_user.get_author_id()))
    if form_data["md"] != None:
      props.append(("body"), markdown(form_data["md"].read().decode("utf-8")))
  
    # build field update
    update_fields = ", ".join([ "{}=?".format(field_label) for field_label, value in props if value != None ])
    params = [ value for _, value in props if value != None  ] + [id]
    print(update_fields, params)
    
    get_db().execute("UPDATE posts SET {} WHERE id=?".format(update_fields), params)
    get_db().commit()

    flash("L'articolo è stato creato correttamente", "primary")
    return redirect(url_for('blog.dashboard'))

  # render view
  return render_template("blog/post_create_update.html",  form = form, post = post, tags = Tags().getList())


@bp_blog.route("/delete/<int:id>")
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