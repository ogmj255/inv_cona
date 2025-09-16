#!/usr/bin/env python3
from pymongo import MongoClient
import bcrypt
from config import MONGO_URI

client = MongoClient(MONGO_URI)
cona_inv = client['cona_inv']
users = cona_inv['users']

# Crear nueva contraseña para admin
password = "admin123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Actualizar admin
users.update_one(
    {'username': 'admin'},
    {'$set': {'password': hashed}}
)

print(f"Contraseña admin actualizada: {password}")

# Verificar
admin_user = users.find_one({'username': 'admin'})
if bcrypt.checkpw(password.encode('utf-8'), admin_user['password'].encode('utf-8')):
    print("Verificacion exitosa")
else:
    print("Error en verificacion")