# seguridad.py
import bcrypt

def hashear_contraseña(password_plana):
    return bcrypt.hashpw(password_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_contraseña(password_plana, password_hash_guardado):
    return bcrypt.checkpw(password_plana.encode('utf-8'), password_hash_guardado.encode('utf-8'))
