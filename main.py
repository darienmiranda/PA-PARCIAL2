from ast import Return
from cmath import pi
from pickletools import read_uint1
from random import random
import string
from turtle import title
from flask import Flask, render_template, request, redirect, url_for, flash
from models import consult_users
from models import register_user
import hashlib
import funciones
import random
import string

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
                else:
                    for user in usuario:
                        if(user['validate'] == 'true'):
                            return redirect(url_for('index')) 
                        else:
                            return render_template("validar/mail.html")


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
            validar_email = funciones.validate_mail(user)
            if validar_email == True:
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
            else:
                isValid = False
                flash("Se ha ingresado un correo no valido")

    if isValid == False:
        return render_template("usuarios/register.html", name=name, user = user, last_name = last_name)
    
    validate = (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
    url_validate = (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(60)))

    password_encrypt = hashlib.sha512(password.encode()).hexdigest()

    register_user.CrearUsuario(nombre=name, apellido=last_name, user=user, password=password_encrypt, validate = validate, url_validate=url_validate)
    
    title = 'VALIDACION DE CUENTA'
    body = '<h5>Su cuenta ha sido registrada con exito <br> Para ativar su cuenta porfavor ingrese <a href="http://127.0.0.1:5000/validar-cuenta/'+url_validate+'?token='+validate+'" style="text-decoration:none; color: blue;">Aquí</a></h5>'

    funciones.send_validate_email(user = user, title = title, body = body)

    return render_template("validar/mail.html")

@app.get("/validar-cuenta/<urluser>")
def validar_cuenta(urluser):
    validate = request.args.get("token")
    usuario = consult_users.ObtenerUsuarioValidar(validate = validate, url_validate=urluser)
    if not usuario:
        return render_template("errores/url_not_exist.html")
    else:
        register_user.UsuarioValidado(validate = validate, url_validate=urluser)
        return render_template("validar/validacion.html")

#RECUPERAR CUENTA
@app.get("/recuperar-cuenta")
def recuperar():
    return render_template("usuarios/recuperar.html")

@app.post("/recuperar-cuenta")
def recuperarPost():
    user = request.form.get('user')
    isValid = True

    if user == "":
        isValid = False
        flash("Ingrese un email")
    else:
        usuario = consult_users.ObtenerUusarioUser(user=user)
        if not usuario:
            isValid = False
            flash("Este email no se encuetra registrado")
            
    if isValid == False:
        return render_template("usuarios/recuperar.html", user = user)
    
    url_pass = (''.join(random.choice(string.ascii_letters + string.digits) for _ in range(60)))
    
    register_user.EnviarUrlPass( user=user, url_pass=url_pass ) 
    
    title = 'Recuperacion de cuenta'
    body = '<h5>Para recuperar su cuenta porfavor ingrese <a href=" http://127.0.0.1:5000/recuperar-cuenta/'+url_pass+'" style="text-decoration:none; color: blue;">Aquí</a></h5>'

    funciones.send_validate_email(user = user, title = title, body = body)
    
    return render_template("validar/password.html")

@app.get("/recuperar-cuenta/<urluser>")
def recuperar_cuenta(urluser):
    if urluser != "": 
        usuario = consult_users.ObtenerUrlPass(url_pass = urluser)
        if not usuario:
            return render_template("errores/url_not_exist.html")
        else:
            return render_template("usuarios/formulario_recuperacion.html", urluser = urluser)

@app.post("/recuperar-cuenta/<urluser>")
def recuperar_cuentaPost(urluser):
    if urluser != "": 
        usuario = consult_users.ObtenerUrlPass(url_pass = urluser)
        if not usuario:
            return render_template("errores/url_not_exist.html")
        else:
            try:
                password1 = request.form.get('password1')
            except:
                password1 = ""
                
            try:
                password2 = request.form.get('password2')
            except:
                password2 = ""
                
            isValid = True
            
            if(password1 == ""):
                isValid = False
                flash("Es necesario que ingrese una contraseña")
            else:
                if(password2 == ""):
                    isValid = False
                    flash("Es necesario que repita la contraseña ingresada")
                else:
                    if password1 != password2:
                        isValid = False
                        flash("Las contraseñas deben ser iguales")
                    else:
                        if len(password1) < 8:
                            isValid = False
                            flash("La contraseña debe contener minimo 8 caracteres")
                        else:
                            SpecialSym =['!','"','#','$','%','&',"'",'(',')','*','+',',','-','.','/',':',';','=','?','@','[',']','^','_','`','{','|','}','~']
                            if not any(char.isdigit() for char in password1):
                                isValid = False
                                flash("La contraseña debe contener almenos un numero")
                            if not any(char.isupper() for char in password1):
                                isValid = False
                                flash("La contraseña debe contener almenos una mayuscula")
                            if not any(char in SpecialSym for char in password1):
                                isValid = False
                                flash("La contraseña debe contener almenos un caracter especial")
    
            if isValid == False:
                return render_template("usuarios/formulario_recuperacion.html", urluser = urluser)
            
            for email in usuario:
                user = email['user']
            password_encrypt = hashlib.sha512(password1.encode()).hexdigest()
            register_user.RecuperarCuenta(url = urluser, password = password_encrypt)
                        
            title = 'Recuperacion exitosa'
            body = '<h5>Su contraseña ha sido cambiada con exito</h5>'
                        
            funciones.send_validate_email(user = user, title = title, body = body)
            
            return render_template("index.html")


app.run(debug=True)