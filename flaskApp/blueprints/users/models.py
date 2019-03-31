from flaskApp.extensions.login_ext import login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flaskApp.db.sqlite import query_db

# ################################################################################
# USER CLASS
# ################################################################################
class User():

  def __repr__(self):
    return f"user model: {self.id}"

  def __init__(self, **kwargs):
      
    # add props
    self.id = kwargs.get("id")
    self.email = kwargs.get("emal")
    self.username = kwargs.get("username")
    self.password = kwargs.get("password")
    self.first_name = kwargs.get("first_name")
    self.last_name = kwargs.get("last_name")
    self.title = kwargs.get("title")
    self.job = kwargs.get("job")
    self.role = kwargs.get("role", "guest")
    self.is_active = kwargs.get("is_active")
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
    return f"{self.title} {self.first_name} { self.last_name}, { self.job}"

  @login_manager.user_loader
  def load_user(id):
    user = query_db("SELECT * FROM users WHERE id = ?", [id], one=True)
    if user:
        return User(**user)
    else:
        return None