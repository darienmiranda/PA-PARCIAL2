from config.database import db

def ObtenerUusarioLogin(user, password):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE user="'+user+'" AND PASSWORD="'+password+'"')

    usuario = cursor.fetchall()
    cursor.close()
    return usuario

def ObtenerUusarioUser(user):
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM usuarios WHERE user="'+user+'"')

    usuario = cursor.fetchall()
    cursor.close()
    return usuario

def CrearUsuario(nombre, apellido, user, password):
    cursor = db.cursor()

    cursor.execute("insert into usuarios(nombre_usuario, apellido_usuario, user, password) values(%s,%s,%s,%s)", (
        nombre, 
        apellido, 
        user, 
        password
    ))

    cursor.close()