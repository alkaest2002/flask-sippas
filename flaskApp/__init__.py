
from flask import Flask

# init app
app = Flask(__name__)

# import extensions
from flaskApp.extensions.cache_ext import attach_cache
from flaskApp.extensions.login_ext import attach_login_manager
from flaskApp.extensions.jinja_ext import attach_jinja
from flaskApp.extensions.blueprints_ext import attach_blueprints
from flaskApp.extensions.db_ext import attach_db

# app factory function
def create_app(cfg = None):
        
  # config app
  if cfg is not None: 
    app.config.from_object(cfg)
  
  # attach cache manager
  attach_cache(app)

  # attach login manager
  attach_login_manager(app)

  # attach jinja
  attach_jinja(app)

  # attach blueprints
  attach_blueprints(app)

  # attach db
  attach_db(app)

  # return app
  return app