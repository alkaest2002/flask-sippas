from flask_mail import Mail

# init mail
mail = Mail()

# attacher
def attach_mail(app):
  mail.init_app(app)