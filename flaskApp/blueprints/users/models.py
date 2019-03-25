from flaskApp.extensions.login_ext import login_manager
from werkzeug.security import check_password_hash, generate_password_hash

# ################################################################################
# USERS
# ################################################################################
USERS = {
  "gualberto" : {
    "_id": "gualberto",
    "author_id": 1,
    "username": "gualberto",
    "password": "pbkdf2:sha256:150000$krAmXdQm$bd6f9e9236009d03ee6d90aba0d13c3f8efb165c060419924c334d9b98f63bd7"
  }
}

# ################################################################################
# USER CLASS
# ################################################################################
class User():

  def __repr__(self):
    return "user model: {}".format(self._id)

  def __init__(self, **kwargs):
      
    # add props
    self._id = kwargs.get('_id', None)
    self.author_id = kwargs.get('author_id', None)
    self.username = kwargs.get('username', None)
    self.password = kwargs.get('password', None)
    self.is_active = True
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
    return self._id

  def get_author_id(self):
    # return author_id
    return self.author_id

  @login_manager.user_loader
  def load_user(_id):
    userObj = USERS[_id] if _id in USERS else None
    return User(**userObj) if userObj else None
  