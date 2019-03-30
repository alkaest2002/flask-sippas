import os

# base config
class Config(object):
  MAX_CONTENT_LENGTH = .5 * 1024 * 1024 # max 512Kb
  WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")

# dev config
class devConfig(Config):
  ENV = "development"
  DEBUG = True
  SECRET_KEY = os.getenv("DEV_SECRET_KEY")

  MAIL_USE_SSL = True
  MAIL_SERVER = os.getenv("DEV_MAIL_SERVER")
  MAIL_PORT = os.getenv("DEV_MAIL_PORT")
  MAIL_USERNAME = os.getenv("DEV_MAIL_USERNAME")
  MAIL_PASSWORD = os.getenv("DEV_MAIL_PASSWORD")

  CACHE_TYPE = os.getenv("DEV_CACHE_TYPE")

# prod config
class prodConfig(Config):  
  SECRET_KEY = os.getenv("PROD_SECRET_KEY")
  CACHE_TYPE = os.getenv("PROD_CACHE_TYPE")