from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

# ################################################################################
# FORMS
# ################################################################################

class LoginForm(FlaskForm):
  
  # username
  username = StringField(
    label = 'Username', 
    validators = [ 
        DataRequired(message="Questo dato è obbligatorio."),
    ],
    render_kw = { "required": False },
    filters=[ lambda x: x and x.lower() ],
  )
  
  # password
  password = PasswordField(
    label = 'Password', 
    render_kw = { "required": False },
    validators = [
        DataRequired(message="Questo dato è obbligatorio."),
    ],
  )