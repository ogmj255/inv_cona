from pymongo import MongoClient
from datetime import datetime
import bcrypt
import os

# Usar la misma configuración que la app
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cona_inv')

try:
    client = MongoClient(MONGO_URI)
    db = client['cona_inv']
    
    # Crear usuario super admin por defecto
    users = db['users']
    if users.count_documents({'username': 'admin'}) == 0:
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = {
            'username': 'admin',
            'password': hashed_password,
            'nombre': 'Super',
            'apellido': 'Administrador',
            'email': 'admin@cona.gov.ec',
            'role': 'super_admin',
            'created_at': datetime.now()
        }
        users.insert_one(admin_user)
        print("Usuario admin creado exitosamente")
    
    # Crear parroquia de ejemplo
    parroquias = db['parroquias']
    if parroquias.count_documents({}) == 0:
        parroquia_ejemplo = {
            'nombre': 'Cuenca',
            'canton': 'Cuenca',
            'codigo': 'CUE001',
            'created_at': datetime.now()
        }
        parroquias.insert_one(parroquia_ejemplo)
        print("Parroquia de ejemplo creada")
    
    print("Base de datos inicializada correctamente")
    
except Exception as e:
    print(f"Error inicializando base de datos: {e}")