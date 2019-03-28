from flaskApp.extensions.login_ext import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flaskApp.db.sqlite import query_db

# ################################################################################
# USER CLASS
# ################################################################################
class User():

  def __repr__(self):
    return "user model: {}".format(self.id)

  def __init__(self, *args):
      
    # add props
    self.id = args[0]
    self.email = args[1]
    self.username = args[2]
    self.password = args[3]
    self.first_name = args[4]
    self.last_name = args[5]
    self.title = args[6]
    self.job = args[7]
    self.role = args[8]
    self.is_active = args[9]
    self.is_anonymous = False
    self.is_authenticated = True
        
  def save(self):
    pass

  def check_pass(self, password):
    # check pass
    # print(generate_password_hash(password))
    return check_password_hash(self.password, password)

  def get_id(self):
    # return id
    return self.id

  def get_author(self):
    # return author name
    return "{} {} {}, {}".format(self.title, self.first_name, self.last_name, self.job)

  @login_manager.user_loader
  def load_user(id):
    user = query_db("SELECT * FROM users WHERE id = ?", [id], one=True)
    if user:
        return User(*user)
    else:
        return None