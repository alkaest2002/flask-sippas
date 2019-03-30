import os

from flaskApp import app
from flask_caching import Cache

# init cache
cache = Cache(config={
  'CACHE_TYPE': app.config["CACHE_TYPE"],
  'CACHE_DEFAULT_TIMEOUT': 60*60*6,
  'CACHE_THRESHOLD': 1000,
  'CACHE_DIR': os.path.join(app.root_path, 'static', 'cache')
})

# attacher
def attach_cache(app):
  cache.init_app(app)