
TAGS = [
  "#Aeronautica",
  "#CorpiDelloStato",
  "#Dipendenze",
  "#Eventi",
  "#Farmaci",
  "#Farmacologia",
  "#Formazione",
  "#ForzeArmate",
  "#Incivolo",
  "#Medicina",
  "#Neuroimaging",
  "#Neuroscienze",
  "#Psichiatria",
  "#Psicologia", 
  "#Salute",
  "#Varie"
]

# ################################################################################
# TAGS CLASS
# ################################################################################
class Tags():

  def __repr__(self):
    return "tags"

  def __init__(self, **kwargs):
      
    # add props
    self.tags = TAGS
        
  def get_list(self):
    return self.tags 