from datetime import date
from datetime import datetime
from OCR import ocr

d1=ocr("date.png")
def date_check(d2):
  
  d2= d2[:-1]
  s=""
  deadline= 365*3+8
  d0 = date.today()
  d2=d2.split("/")
  if (len(d2[2])==2):
    d2[2]="20"+d2[2]
  d1 = date(int(d2[2]), int(d2[1]), int(d2[0]))
  delta = d0- d1
  if (delta.days > deadline):
    s="Expiré depuis " + str(delta.days-deadline)+ " jours!"
  else:
    s="date Valide pour encore "+ str(deadline-delta.days)+ " jours!"

  return(s)
