#!/usr/bin/env python3
from pymongo import MongoClient
import bcrypt
from config import MONGO_URI

client = MongoClient(MONGO_URI)
cona_inv = client['cona_inv']
users = cona_inv['users']

# Probar login del admin
admin_user = users.find_one({'username': 'admin'})
if admin_user:
    print(f"Usuario admin encontrado")
    print(f"Contraseña almacenada: {admin_user['password'][:50]}...")
    
    # Probar verificación
    test_password = "admin123"
    stored_password = admin_user['password']
    
    try:
        if bcrypt.checkpw(test_password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Contraseña verificada correctamente")
        else:
            print("Contraseña incorrecta")
    except Exception as e:
        print(f"Error verificando contraseña: {e}")
else:
    print("Usuario admin no encontrado")