#!/usr/bin/env python3
from pymongo import MongoClient
import bcrypt
from datetime import datetime
from bson.objectid import ObjectId
from config import MONGO_URI

client = MongoClient(MONGO_URI)
cona_inv = client['cona_inv']
users = cona_inv['users']
parroquias = cona_inv['parroquias']

# Obtener algunas parroquias para asignar técnicos
parroquias_list = list(parroquias.find().limit(3))

tecnicos = [
    {
        'username': 'tecnico_quito',
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'email': 'juan.perez@cona.gov.ec',
        'role': 'tecnico',
        'parroquia_id': parroquias_list[0]['_id'] if parroquias_list else None,
        'created_at': datetime.now()
    },
    {
        'username': 'tecnico_guayaquil',
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'nombre': 'María',
        'apellido': 'González',
        'email': 'maria.gonzalez@cona.gov.ec',
        'role': 'tecnico',
        'parroquia_id': parroquias_list[1]['_id'] if len(parroquias_list) > 1 else None,
        'created_at': datetime.now()
    },
    {
        'username': 'tecnico_cuenca',
        'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'nombre': 'Carlos',
        'apellido': 'Rodríguez',
        'email': 'carlos.rodriguez@cona.gov.ec',
        'role': 'tecnico',
        'parroquia_id': parroquias_list[2]['_id'] if len(parroquias_list) > 2 else None,
        'created_at': datetime.now()
    }
]

print("Creando técnicos de ejemplo...")

for tecnico in tecnicos:
    # Verificar si ya existe
    if not users.find_one({'username': tecnico['username']}):
        users.insert_one(tecnico)
        parroquia_nombre = "Sin asignar"
        if tecnico['parroquia_id']:
            parroquia = parroquias.find_one({'_id': tecnico['parroquia_id']})
            if parroquia:
                parroquia_nombre = parroquia['nombre']
        
        print(f"Tecnico creado: {tecnico['username']} - {tecnico['nombre']} {tecnico['apellido']} - Parroquia: {parroquia_nombre}")
    else:
        print(f"- Técnico ya existe: {tecnico['username']}")

print("\nTécnicos creados exitosamente!")
print("Credenciales: usuario/admin123")