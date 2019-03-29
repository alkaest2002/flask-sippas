
from flask import request, render_template, flash, redirect, url_for, abort, current_app
from flask_login import current_user, login_user, login_required, logout_user, current_user
from flaskApp.db.sqlite import query_db
from flaskApp.utils.decorators import has_role

from . import bp_users
from .models import User 
from .forms import *

# ################################################################################
# ROUTES
# ################################################################################

# -----------------------------------------------------------------
# UNAUTHORIZED
# -----------------------------------------------------------------
@bp_users.route("/unauthorized")
def unauthorized():

  # render view
  return render_template('users/unauthorized.html')

# -----------------------------------------------------------------
# LOGIN
# -----------------------------------------------------------------
@bp_users.route("/login", methods=("get", "post"))
@has_role(["guest"])
def login():

    # init form
    form = LoginForm()

    # on validate
    if form.validate_on_submit():

      # cache form data
      form_data = form.data

      # fetch user
      user = query_db("SELECT * FROM users WHERE username = ?", [form_data["username"]], one=True)
      
      # no user found
      if user is None:
          
        # flash error
        flash("<b>Oops!</b> Username non presente nel server.", "danger")
        
        # redirect to login
        return redirect(url_for('users.login'))
       
      # istantiate user
      user = User(**user)

      # if password is invalid
      if not user.check_pass(form_data["password"]):
          
          # flash error
          flash("<b>Oops!</b> Credenziali non valide.", "danger")
          
          # redirect to login
          return redirect(url_for('users.login'))
      
      # login user
      login_user(user)

      # redirect to home
      return redirect(url_for('blog.dashboard'))

    # render view
    return render_template("users/login.html", form = form )

# -----------------------------------------------------------------
# LOGOUT
# -----------------------------------------------------------------
@bp_users.route("/logout")
@login_required
def logout():
    
  # logout user
  logout_user()
  
  # redirect to login page
  return redirect(url_for('users.login'))