import os
from flaskApp import create_app
    
# create app
app = create_app("config.devConfig")

# run app
if __name__ == "__main__":
  app.run()