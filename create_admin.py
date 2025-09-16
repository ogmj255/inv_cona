from pymongo import MongoClient
import bcrypt
from datetime import datetime
from config import MONGO_URI

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['cona_inv']
users = db['users']

# Crear usuario super admin
admin_user = {
    'username': 'admin',
    'password': bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()),
    'nombre': 'Super',
    'apellido': 'Administrador',
    'email': 'admin@cona.gov.ec',
    'role': 'super_admin',
    'created_at': datetime.now()
}

# Eliminar admin existente si existe
users.delete_one({'username': 'admin'})

# Insertar nuevo admin
users.insert_one(admin_user)

print("Usuario super admin creado exitosamente:")
print("Usuario: admin")
print("Contraseña: admin123")