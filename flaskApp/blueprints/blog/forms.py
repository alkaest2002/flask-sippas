from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, BooleanField
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired

from .models import Tags

CHOICES = list(map(lambda x: (x,x), Tags().getList()))

class MultiCheckboxField(SelectMultipleField):
	widget = ListWidget(prefix_label=False)
	option_widget	= CheckboxInput()

# ################################################################################
# FORMS
# ################################################################################

class PostCreateForm(FlaskForm):
  
  # title
  title = StringField(
    label = 'Titolo', 
    validators = [ 
      DataRequired(message="Questo dato è obbligatorio."),
    ],
    render_kw = { "required": False },
  )

  # tags
  tags = MultiCheckboxField(
    'Tag', 
    choices=CHOICES,
    validators = [ 
      DataRequired(message="Questo dato è obbligatorio."),
    ],
  )

  # is sticky
  is_sticky = BooleanField(
    label = 'Articolo in evidenza'
  )

  # teaser image
  teaser = FileField(
    label = 'Immagine teaser',
  )

  # markdown text
  md = FileField(
    label = "Testo dell'articolo",
    validators=[
      FileRequired(message="Questo file è obbligatorio")
    ]
  )

class PostUpdateForm(PostCreateForm):
  
  # markdown text
  md = FileField(
    label = "Testo dell'articolo",
    validators=[]
  )

  