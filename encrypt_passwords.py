#!/usr/bin/env python3
"""
Script para encriptar todas las contraseñas existentes en la base de datos
"""

from pymongo import MongoClient
import bcrypt
from config import MONGO_URI

def encrypt_all_passwords():
    client = MongoClient(MONGO_URI)
    cona_inv = client['cona_inv']
    users = cona_inv['users']
    
    # Obtener todos los usuarios
    all_users = list(users.find({}))
    
    print(f"Encontrados {len(all_users)} usuarios para actualizar...")
    
    for user in all_users:
        username = user['username']
        current_password = user['password']
        
        # Solo actualizar si la contraseña no está ya encriptada con bcrypt
        if not (isinstance(current_password, str) and current_password.startswith('$2b$')):
            # Determinar la contraseña en texto plano
            plain_password = None
            
            if isinstance(current_password, str):
                if current_password.startswith('scrypt:') or current_password.startswith('$2b$'):
                    print(f"Saltando {username} - ya encriptado")
                    continue
                else:
                    # Contraseña en texto plano
                    plain_password = current_password
            elif isinstance(current_password, dict) and 'data' in current_password:
                print(f"Saltando {username} - formato binario no soportado")
                continue
            elif isinstance(current_password, bytes):
                try:
                    plain_password = current_password.decode('utf-8')
                except:
                    print(f"Error decodificando contraseña para {username}")
                    continue
            
            if plain_password:
                # Encriptar la contraseña
                hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Actualizar en la base de datos
                users.update_one(
                    {'_id': user['_id']},
                    {'$set': {'password': hashed_password}}
                )
                print(f"Contraseña actualizada para: {username}")
            else:
                print(f"No se pudo procesar la contraseña para: {username}")
    
    print("\n¡Proceso completado!")
    print("Todas las contraseñas han sido encriptadas con bcrypt.")

if __name__ == '__main__':
    encrypt_all_passwords()