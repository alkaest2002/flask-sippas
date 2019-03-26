import re

from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, BooleanField, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Regexp, Optional, Length, DataRequired

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
      DataRequired(message="Il titolo è obbligatorio."),
      Length(max=100, message="Il titolo è troppo lungo (max 100 caratteri).")
    ],
    render_kw = { "required": False },
  )

  # tags
  tags = MultiCheckboxField(
    'Tag', 
    choices=CHOICES,
    validators = [ 
      DataRequired(message="Le etichette sono obbligatorie (almeno una)."),
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
  )

  # --------------------------------------------------------------------------
  # Custom validations
  # --------------------------------------------------------------------------

  def validata_is_sticky(form, field):
    if field.data == None: return
    if form.teaser.data == None:
      raise ValidationError('Gli articoli in evidenza devono avere un"immagine')

  def validate_tags(form, field):
    if field.data == None: return
    accepted_tags = Tags().getList()
    if not all(elem in accepted_tags for elem in field.data):
      raise ValidationError('Etichette non riconosciute.')
    if len(field.data) > 3:
      raise ValidationError('Massimo tre etichette consentite.')

  def validate_teaser(form, field):
    pattern = re.compile(r"[^\\]*\.(jpg|jpeg|gif|png)$")
    if field.data == None: return
    if not pattern.match(field.data.filename):
      raise ValidationError('Tipo di immagine non compatibile.')

  def validate_md(form, field):
    pattern = re.compile(r"[^\\]*\.(md|txt)$")
    if field.data == None: return
    if not pattern.match(field.data.filename):
      raise ValidationError('Tipo di file markdown non compatibile.')

class PostUpdateForm(PostCreateForm):
  
  # markdown text
  md = FileField(
    label = "Testo dell'articolo",
    validators = []
  )

  