from pymongo import MongoClient
from config import MONGO_URI

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['cona_inv']
users = db['users']

# Actualizar usuario admin con contraseña en texto plano
users.update_one(
    {'username': 'admin'},
    {'$set': {'password': 'admin123'}}
)

print("Contraseña del admin actualizada a texto plano: admin123")