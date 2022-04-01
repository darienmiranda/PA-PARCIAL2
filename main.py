from cmath import pi
from flask import Flask, render_template, request, redirect, url_for, flash
from models import consult_users
import hashlib

app = Flask(__name__)
app.secret_key = 'fjifjidfjied5df45df485h48@'

@app.get("/")
def index():
    return render_template("index.html")

#LOGIN
@app.get("/login")
def login():
    return render_template("usuarios/login.html")

@app.post("/login")
def loginPost():
    user = request.form.get('user')
    
    try:
        password = request.form.get('password')
    except:
        password = ""
        
    isValid = True

    if user == "":
        isValid = False
        flash("Ingrese un Email")
    else:
        usuario = consult_users.ObtenerUusarioUser(user=user)
        if not usuario:
            isValid = False
            flash("El email no se encuentra registrado")
        else:
            if password == "":
                isValid = False
                flash("Ingrese la contraseña")
            else:
                password_encrypt = hashlib.sha512(password.encode()).hexdigest()
                usuario = consult_users.ObtenerUusarioLogin(user=user, password=password_encrypt)
                if not usuario:
                    isValid = False
                    flash("Contraseña incorrecta")

    if isValid == False:
        return render_template("usuarios/login.html", user = user)

    return redirect(url_for('index'))

#REGISTROOOOO
@app.get("/register")
def register():
    return render_template("usuarios/register.html")

@app.post("/register")
def registerPost():
    name = request.form.get('name')
    user = request.form.get('user')
    last_name = request.form.get('last_name')
    try:
        password = request.form.get('password')
    except:
        password = ""

    isValid = True

    if name == "":
        isValid = False
        flash("debe ingresar un nombre")
    else:
        if user == "":
            isValid = False
            flash("debe ingresar un Email")
        else:
            usuario = consult_users.ObtenerUusarioUser(user=user)
            if not usuario:
                if password == "":
                    isValid = False
                    flash("Ingrese una contraseña")
                else:
                    if len(password) < 8:
                        isValid = False
                        flash("La contraseña debe contener minimo 8 caracteres")
                    else:
                        SpecialSym =['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','=','?','@','[',']','^','_','`','{','|','}','~']
                        if not any(char.isdigit() for char in password):
                            isValid = False
                            flash("La contraseña debe contener almenos un numero")
                        if not any(char.isupper() for char in password):
                            isValid = False
                            flash("La contraseña debe contener almenos una mayuscula")
                        if not any(char in SpecialSym for char in password):
                            isValid = False
                            flash("La contraseña debe contener almenos un caracter especial")
            else:
                isValid = False
                flash("El Email ya se encuentra registrado")

    if isValid == False:
        return render_template("usuarios/register.html", name=name, user = user, last_name = last_name)

    password_encrypt = hashlib.sha512(password.encode()).hexdigest()

    consult_users.CrearUsuario(nombre=name, apellido=last_name, user=user, password=password_encrypt)


    return redirect(url_for('index')) 

app.run(debug=True)