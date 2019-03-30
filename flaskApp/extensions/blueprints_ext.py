from flask import render_template, jsonify

from flaskApp.blueprints.main import bp_main
from flaskApp.blueprints.users import bp_users
from flaskApp.blueprints.blog import bp_blog

# attacher
def attach_blueprints(app):

  #-----------------------------------------------------------------------------
  # register routes
  #-----------------------------------------------------------------------------
  app.register_blueprint(bp_main, url_prefix='/')
  app.register_blueprint(bp_users, url_prefix='/users')
  app.register_blueprint(bp_blog, url_prefix='/blog')
  
  #-----------------------------------------------------------------------------
  # error handlers
  #-----------------------------------------------------------------------------
  @app.errorhandler(400)
  @app.errorhandler(401)
  @app.errorhandler(403)
  @app.errorhandler(404)
  @app.errorhandler(500)
  @app.errorhandler(413)
  def page_error(error):
    return render_template('error.html', error=error)