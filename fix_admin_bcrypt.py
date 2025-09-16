#!/usr/bin/env python3
"""
Script para asegurar que el usuario admin tenga contraseña encriptada
"""

from pymongo import MongoClient
import bcrypt
from config import MONGO_URI

def fix_admin_password():
    client = MongoClient(MONGO_URI)
    cona_inv = client['cona_inv']
    users = cona_inv['users']
    
    # Buscar usuario admin
    admin_user = users.find_one({'username': 'admin'})
    
    if admin_user:
        current_password = admin_user['password']
        print(f"Usuario admin encontrado. Contraseña actual: {type(current_password)}")
        
        # Verificar si ya está encriptada con bcrypt
        if isinstance(current_password, str) and current_password.startswith('$2b$'):
            print("La contraseña del admin ya está encriptada con bcrypt")
            return
        
        # Encriptar contraseña "admin123"
        new_password = "admin123"
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Actualizar en la base de datos
        users.update_one(
            {'username': 'admin'},
            {'$set': {'password': hashed_password}}
        )
        
        print(f"Contraseña del admin actualizada y encriptada con bcrypt")
        print(f"Nueva contraseña: {new_password}")
        
    else:
        print("Usuario admin no encontrado")

if __name__ == '__main__':
    fix_admin_password()