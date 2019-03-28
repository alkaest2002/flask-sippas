
from flask_login import LoginManager

# init flask-login
login_manager = LoginManager()

# anonymous user class
class MyAnonymousUser():
    
  def __init__(self):
    self.is_active = False
    self.is_anonymous = True
    self.role = 'guest'
    self.is_authenticated = False

  def get_id(self):
    return None

  def __repr__(self):
    return "MyAnonymousUser"

# attacher
def attach_login_manager(app):
   
  # add login_manager to app
  login_manager.init_app(app)
  login_manager.anonymous_user = MyAnonymousUser
  login_manager.login_view = "users.login"
  login_manager.login_message = u"Effettua il login per accedere a questa risorsa."
  login_manager.login_message_category = "hide"