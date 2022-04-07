from config.database import db

def CrearUsuario(nombre, apellido, user, password, validate, url_validate):
    cursor = db.cursor()
    cursor.execute("insert into usuarios(nombre_usuario, apellido_usuario, user, password, validate, url_val_mail) values(%s,%s,%s,%s,%s,%s)", (
        nombre, 
        apellido, 
        user, 
        password,
        validate,
        url_validate
    ))
    cursor.close()

def UsuarioValidado(validate, url_validate):
    cursor = db.cursor()
    cursor.execute('UPDATE usuarios SET validate = "true", url_val_mail = "" WHERE validate="'+validate+'" AND url_val_mail="'+url_validate+'"')
    cursor.close()
    
def EnviarUrlPass(user, url_pass):
    cursor = db.cursor()
    cursor.execute('UPDATE usuarios SET url_pass = "'+url_pass+'" WHERE user="'+user+'" ')
    cursor.close()

def RecuperarCuenta(url, password):
    cursor = db.cursor()
    cursor.execute('UPDATE usuarios SET password = "'+password+'", url_pass="" WHERE url_pass="'+url+'" ')
    User = cursor.fetchone()
    
    cursor.close()
    return User