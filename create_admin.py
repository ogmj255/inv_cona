import bcrypt
from pymongo import MongoClient
from datetime import datetime

# Conectar a MongoDB
client = MongoClient('mongodb+srv://ogmoscosoj2:mQaZ63iaQO7feFXo@conagoparedbinventario.ecb0dj0.mongodb.net/?retryWrites=true&w=majority&appName=conagoparedbinventario')
db = client['cona_inv']
users = db['users']

# Crear usuario admin
password = '123'
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

admin_user = {
    'username': 'admin',
    'password': hashed_password,
    'nombre': 'Administrador',
    'apellido': 'Sistema',
    'email': 'admin@cona.gov.ec',
    'role': 'super_admin',
    'parroquia_id': None,
    'created_at': datetime.now()
}

# Eliminar admin existente si existe
users.delete_one({'username': 'admin'})

# Insertar nuevo admin
result = users.insert_one(admin_user)
print(f"Usuario admin creado con ID: {result.inserted_id}")
print("Usuario: admin")
print("Contraseña: 123")