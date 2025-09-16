#!/usr/bin/env python3
from pymongo import MongoClient
import bcrypt
from config import MONGO_URI

client = MongoClient(MONGO_URI)
cona_inv = client['cona_inv']
users = cona_inv['users']

# Contraseñas por defecto
default_passwords = {
    'admin': 'admin123',
    'admin_quito': 'admin123',
    'admin_guayaquil': 'admin123', 
    'admin_cuenca': 'admin123'
}

all_users = list(users.find({}))
print(f"Reseteando contraseñas para {len(all_users)} usuarios...")

for user in all_users:
    username = user['username']
    
    # Usar contraseña por defecto o admin123
    password = default_passwords.get(username, 'admin123')
    
    # Encriptar
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Actualizar
    users.update_one(
        {'_id': user['_id']},
        {'$set': {'password': hashed}}
    )
    
    print(f"Usuario: {username} - Contraseña: {password}")

print("\nTodas las contraseñas han sido reseteadas y encriptadas.")