import os
from dotenv import load_dotenv
from pathlib import Path

# load .env
load_dotenv(dotenv_path=Path('.') / '.env')

# base config
class Config(object):
  MAX_CONTENT_LENGTH = .5 * 1024 * 1024 # max 512Kb
  DATABASE = os.getenv("SQLITE_DB")
  WTF_CSRF_SECRET_KEY = os.getenv("WTF_CSRF_SECRET_KEY")

# dev config
class devConfig(Config):
  
  ENV = "development"
  DEBUG = True
  SECRET_KEY = os.getenv("DEV_SECRET_KEY")

  MAIL_SERVER = os.getenv("DEV_MAIL_SERVER")
  MAIL_PORT = os.getenv("DEV_MAIL_PORT")
  MAIL_USE_SSL = True
  MAIL_USERNAME = os.getenv("DEV_MAIL_USERNAME")
  MAIL_PASSWORD = os.getenv("DEV_MAIL_PASSWORD")

# prod config
class prodConfig(Config):
  
  SECRET_KEY = os.getenv("PROD_SECRET_KEY")