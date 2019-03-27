
from flask import request, render_template, flash, redirect, url_for, abort, current_app
from flask_login import current_user, login_user, login_required, logout_user, current_user

from . import bp_users
from .models import USERS, User 
from .forms import *

# ################################################################################
# BEFORE EACH REQUEST
# ################################################################################

@bp_users.before_request
def before_request():

  # logged in users may not visit login/register page
  if current_user.is_authenticated and request.endpoint in [ 'users.login' ]:
    return redirect(url_for('main.index'))


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
def login():

    # init form
    form = LoginForm()

    # on validate
    if form.validate_on_submit():

      # fetch user
      userObj = USERS[form.username.data] if form.username.data in USERS else None
      
      # no user found
      if userObj is None:
          
        # flash error
        flash("<b>Oops!</b> Username non presente nel server.", "error")
        
        # redirect to login
        return redirect(url_for('users.login'))
            
      # istantiate user
      user = User(**userObj)

      # if credentials are invalid
      if not user.check_pass(form.password.data):
          
          # flash error
          flash("<b>Oops!</b> Credenziali non valide.", "error")
          
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