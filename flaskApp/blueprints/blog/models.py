
TAGS = [
  "#Aeronautica",
  "#Benessere",
  "#Formazione",
  "#Dipendenze",
  "#Eventi",
  "#Incivolo",
  "#ForzeArmate",
  "#Medicina",
  "#Neuroscienze",
  "#NeuroImaging",
  "#Psichiatria",
  "#Psicologia", 
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