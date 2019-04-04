from flask import render_template
from werkzeug.exceptions import HTTPException

from flaskApp.blueprints.main import bp_main
from flaskApp.blueprints.gild import bp_gild
from flaskApp.blueprints.users import bp_users
from flaskApp.blueprints.blog import bp_blog
from flaskApp.blueprints.api import bp_api

# simple generic error class
class GenericError:
  def __init__(self):
    self.code = 500
    self.description = "Generic server error. Please, report this error to the webmaster."

# attacher
def attach_blueprints(app):

  #-----------------------------------------------------------------------------
  # register routes
  #-----------------------------------------------------------------------------
  app.register_blueprint(bp_main, url_prefix='/')
  app.register_blueprint(bp_gild, url_prefix='/gild')
  app.register_blueprint(bp_users, url_prefix='/users')
  app.register_blueprint(bp_blog, url_prefix='/blog')
  app.register_blueprint(bp_api, url_prefix='/api')
  
  #-----------------------------------------------------------------------------
  # errors handler
  #-----------------------------------------------------------------------------
  @app.errorhandler(Exception)
  def page_error(error):
    print(error)
    if not isinstance(error, HTTPException): 
      error = GenericError()
    return render_template('error.html', error=error), error.code