import os
from flaskApp import create_app

# type of environement
cfg = os.environ.get("CFG", "devConfig")
    
# create app
app = create_app("config.{}".format(cfg))

# run app
app.run()