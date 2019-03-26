
import mistune
from base64 import b64encode

# init markdown
markdown = mistune.Markdown()

def format_datetime(value, format="%d %b %Y %I:%M %p"):    
  if value is None: return ""
  return value.strftime(format)

def md_to_html(value):
  return markdown(value)

def btoa(value):
  if value is None: return ""
  return b64encode(bytes(value, 'utf-8')).decode("utf-8")

# attacher
def attach_jinja(app):
  app.jinja_env.filters['to_data_time'] = format_datetime
  app.jinja_env.filters['md_to_html'] = md_to_html
  app.jinja_env.filters['b64_encode'] = btoa