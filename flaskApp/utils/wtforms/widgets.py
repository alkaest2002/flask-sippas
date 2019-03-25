

class Formfield_table:

  def __init__(self):
   pass

  def __call__(self, field, **kwargs):
    html = []
    kwargs.setdefault("id", field.id)
    parent_index = kwargs.get("parent_loop")
    html.append('<div class="row">')
    for subfield in field:
      html.append(
        '''
        <div class="col">
          <div class="form-group mb-1">
            {}
          </div>
        </div>'''.format(subfield(placeholder="iterazione #{}".format(parent_index))))
    html.append("</div>")
    if field.errors:
      html.append('<div class="mb-3"><small class="text-danger">errore negli orari riportati qui sopra.</small></div>')
    return "".join(html)