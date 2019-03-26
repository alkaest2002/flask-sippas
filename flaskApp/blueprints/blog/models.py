
TAGS = [
  "#Aeronautica",
  "#Benessere",
  "#CorpiDelloStato",
  "#Dipendenze",
  "#Eventi",
  "#Farmaci",
  "#Farmacologia",
  "#Formazione",
  "#ForzeArmate",
  "#Incivolo",
  "#Medicina",
  "#Neuroscienze",
  "#NeuroImaging",
  "#Psichiatria",
  "#Psicologia", 
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
        
  def getList(self):
    return self.tags 