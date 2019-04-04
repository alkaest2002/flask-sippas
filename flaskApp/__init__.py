
import datetime

from flask import Flask, request
from dotenv import load_dotenv

# load .env variables
env_path = './.env'
load_dotenv(dotenv_path=env_path)

# init app
app = Flask(__name__)

# add cookie
@app.after_request
def after_request(response):
  if request.path != "/":
    response.set_cookie("sippas_cookie_consent", value="set",  expires=datetime.datetime.now() + datetime.timedelta(days=365))
  return response

# config app
app.config.from_object("config.devConfig")
 
# import extensions
from flaskApp.extensions.cache_ext import attach_cache
from flaskApp.extensions.login_ext import attach_login_manager
from flaskApp.extensions.jinja_ext import attach_jinja
from flaskApp.extensions.blueprints_ext import attach_blueprints
from flaskApp.extensions.db_ext import attach_db

# app factory function
def create_app():
         
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