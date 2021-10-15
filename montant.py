from OCR import ocr
s=ocr("lettres.png")

n=''
s = s.replace('\n', '').replace('\r', '')
s= s.split(' ')
for i in range(len(s)):
    s[i].replace(' ', '')
s= n.join(s)
s.replace(' ', '')
print(s)

s1=ocr("chiffres.png")
special_characters1 = ","

if any(c in special_characters1 for c in s1):
  
   s1 = s1.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
   s1 = s1.split(",")
   del(s1[-1])
   s1=n.join(s1)
special_characters2 = "."
if any(c in special_characters2 for c in s1):
  
   s1 = s1.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')
   s1 = s1.split(".")
   del(s1[-1])
   s1=n.join(s1)

print(s1)
import sys,cgi
bases=[("milliards",1e9),("millions",1e6),("milles",1e3),("cent",1e2),("quatre vingt",80),("soixante",60),("cinquante",50),("quarante",40),("trente",30),("vingt",20),("dix",10)]
units=["zero","un","deux","trois","quatre","cinq","six","sept","huit","neuf",None,"onze","douze","treize","quatorze","quinze","seize"]
def flous(value,skip=-1):
    if value < len(units) and units[value]:
        return [] if value <= skip else [units[value]]
    for name,v in bases:
        if value>=v:
            return flous(int(value/v),1 if v <= 1000 else -1) + [name] + flous(int(value%v), 0)
s1=n.join(flous(int(s1)))
print(s1)
k=0   
#if(s==s1):
    #print("ok")
for i in range(len(s1)):
    if(s1[i]==s[i]):
        k+=1
r=k/len(s1)
if(r>0.8):
        print("montant conforme!")
else:
    print("montant non conforme!")