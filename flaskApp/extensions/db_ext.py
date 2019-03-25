from flaskApp.db.sqlite import close_db

# close connection on teardown
def attach_db(app):
 app.teardown_appcontext(close_db)
  