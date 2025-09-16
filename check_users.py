import os
import bcrypt
from pymongo import MongoClient

# Usar la misma URI que la app
mongo_uri = os.environ.get('MONGODB_URI', 'mongodb+srv://ogmoscosoj:KcB4gSO579gBCSzY@conagoparedb.vwmlbqg.mongodb.net/?retryWrites=true&w=majority&appName=conagoparedb')

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    client.admin.command('ping')
    print("✅ Conectado a MongoDB")
    
    db = client['conagoparedb']
    users = db['users_db']
    
    # Verificar usuarios existentes
    print("\n📋 Usuarios existentes:")
    for user in users.find():
        print(f"- Username: {user.get('username')}, Role: {user.get('role')}")
    
    # Crear usuario super_admin si no existe
    if not users.find_one({'username': 'admin'}):
        print("\n🔧 Creando usuario admin...")
        hashed_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        admin_user = {
            'username': 'admin',
            'password': hashed_password,
            'nombre': 'Super',
            'apellido': 'Administrador',
            'email': 'admin@cona.gov.ec',
            'role': 'super_admin'
        }
        users.insert_one(admin_user)
        print("✅ Usuario admin creado")
    else:
        print("ℹ️ Usuario admin ya existe")
    
    # Crear parroquia ejemplo si no existe
    parroquias = db['parroquias']
    if not parroquias.find_one():
        parroquia = {
            'nombre': 'Cuenca',
            'canton': 'Cuenca',
            'codigo': 'CUE001'
        }
        parroquias.insert_one(parroquia)
        print("✅ Parroquia ejemplo creada")
    
    print("\n🎯 Prueba login con: admin / admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")