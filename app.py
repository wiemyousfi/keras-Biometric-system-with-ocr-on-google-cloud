from flask import Flask , render_template ,request, redirect, url_for, flash
from werkzeug.wrappers import Request, Response
from werkzeug.utils import secure_filename
import cv2
import matplotlib.pyplot as plt
from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops
import numpy as np
from PIL import Image
from flask_sqlalchemy import SQLAlchemy
import smtplib
from flask import Flask
from flask_mail import Mail,Message
from flask_mysqldb import MySQL
from flask_login import LoginManager
app= Flask(__name__)
app.secret_key = "Secret Key"
 
#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:wiwi123@localhost/utilisateurs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Data1(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
                          
    def __init__(self,img, name, mimetype):
        
        self.img = img
        self.name = name
        self.mimetype = mimetype
@app.route('/upload', methods=['POST'])
def upload():
    
    pic = request.files['dos']
    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400
    
    img = Data1(img=pic.read(),name=filename, mimetype=mimetype)
    db.session.add(img)
    db.session.commit()
    
    
    image= Image.open(pic)
    img=np.array(image)
    img2=cv2.resize(img,(945,359))
    blobs_labels = measure.label(img2, background=1)
    s=""
    total_area = 0
    counter = 0
    for region in regionprops(blobs_labels):
        if (region.area > 20):
            
            counter +=1
    if (counter>1):
        s=" le dos du chèque est bien validé!"
    else:
        s=" le dos du chèque n'est pas validé!"
    #return 'Img Uploaded!', 200
    #s=""
    #s+=filename+mimetype
    #return (filename)
    flash(s)
    #return(s)
    return redirect(url_for('telecharg'))




class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    psw = db.Column(db.String(100))
   
 
 
    def __init__(self, name, psw):
 
        self.name = name
        self.psw = psw

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Data.query.get(int(id))

@app.route('/signup_post', methods=['GET','POST'])
def signup_post():
    pseudo = request.form.get('name')
    mdp = request.form.get('psw')

    exists1 = db.session.query(db.exists().where(Data.name == pseudo)).scalar()
    exists2 = db.session.query(db.exists().where(Data.psw == mdp)).scalar()
    if exists1 & exists2:
         return redirect(url_for('telecharg'))
    else:
        flash("Accés refusé!")
        return redirect(url_for('util'))



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
 
    if request.method == 'POST':
 
        name = request.form['name']
        psw = request.form['psw']
        
 
 
        my_data = Data(name, psw)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employé ajouté avec succées")
 
        return redirect(url_for('crud'))

#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
 
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.psw = request.form['psw']
        
 
        db.session.commit()
        flash("Employé modifié avec succées")



        return redirect(url_for('crud'))

#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employé supprimé avec succées")
 
    return redirect(url_for('crud'))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/send_message',methods=['POST','GET'])
def form():
    nom= request.form.get("nom")
    mail= request.form.get("mail")
    msg= request.form.get("msg")
    s=""
    s+=nom +"\n"
    s+=mail +"\n"
    s+=msg
    
    message=s
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login("ilefverif@gmail.com","verif++123")
    server.sendmail("ilefverif@gmail.com","ilefverif@gmail.com",message)
    
    flash(" Votre message est bien envoyé")
 
    return redirect(url_for('contact'))

@app.route('/choisir')
def choisir():
    return render_template("choisir.html")

@app.route('/util')
def util():
    return render_template("utilisateur.html")

@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/telecharg')
def telecharg():
    return render_template("telecharg.html")

@app.route('/crud')
def crud():
    all_data = Data.query.all()
    
    return render_template('crd.html', employees = all_data)
    
   
    
if __name__=="__main__":
    app.run()

