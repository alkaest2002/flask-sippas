import re

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, BooleanField, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Regexp, Optional, Length, DataRequired

from .models import Tags

TAGS_CHOICES = list(map(lambda x: (x,x), Tags().get_list()))

# ################################################################################
# FORMS
# ################################################################################

class PostsSearchForm(FlaskForm):

  # title
  title = StringField(
    label = 'Titolo', 
    validators = [ 
      DataRequired(message="Il titolo è obbligatorio."),
      Length(max=150, message="Il titolo è troppo lungo (max 150 caratteri).")
    ]
  )

class PostCreateForm(FlaskForm):
  
  # title
  title = StringField(
    label = 'Titolo', 
    validators = [ 
      DataRequired(message="Il titolo è obbligatorio."),
      Length(max=150, message="Il titolo è troppo lungo (max 150 caratteri).")
    ],
    render_kw = { "required": False },
  )

  # tags
  tags = SelectMultipleField(
    'Tag', 
    choices=TAGS_CHOICES,
    validators = [ 
      DataRequired(message="Le etichette sono obbligatorie (almeno una)."),
    ],
    widget = ListWidget(prefix_label=False),
	  option_widget	= CheckboxInput()
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
  )

  # --------------------------------------------------------------------------
  # Custom validations
  # --------------------------------------------------------------------------

  def validate_is_sticky(form, field):
    if not field.data: return
    if not form.teaser.data:
      raise ValidationError('Gli articoli in evidenza devono avere un"immagine')

  def validate_tags(form, field):
    if not field.data: return
    accepted_tags = Tags().get_list()
    if not all(elem in accepted_tags for elem in field.data):
      raise ValidationError('Etichette non riconosciute.')
    if len(field.data) > 3:
      raise ValidationError('Massimo tre etichette consentite.')

  def validate_teaser(form, field):
    if not field.data: return
    pattern = re.compile(r"[^\\#]*\.(jpg|jpeg|gif|png)$")
    if not pattern.match(field.data.filename):
      raise ValidationError('Tipo di immagine non compatibile.')

  def validate_md(form, field):
    if not field.data: return
    pattern = re.compile(r"[^\\]*\.(md|txt)$")
    if not pattern.match(field.data.filename):
      raise ValidationError('Tipo di file markdown non compatibile.')

class PostUpdateForm(PostCreateForm):
  
  # markdown text
  md = FileField(
    label = "Testo dell'articolo",
    validators = []
  )

  # non need to vcustom validate is_sticky on update
  def validate_is_sticky(form, field):
    pass


  