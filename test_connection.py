#!/usr/bin/env python3
"""
Script para verificar la conexión a MongoDB
"""

from pymongo import MongoClient
import sys

def test_mongodb_connection():
    """Verificar conexión a MongoDB"""
    try:
        print("Verificando conexion a MongoDB...")
        
        # Intentar conectar
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
        
        # Verificar que el servidor responde
        client.admin.command('ping')
        print("Conexion a MongoDB exitosa")
        
        # Verificar base de datos
        db = client['inventario_cona']
        collections = db.list_collection_names()
        print(f"Base de datos 'inventario_cona' encontrada")
        print(f"Colecciones disponibles: {collections}")
        
        # Verificar datos
        users_count = db.users.count_documents({})
        parroquias_count = db.parroquias.count_documents({})
        inventarios_count = db.inventarios.count_documents({})
        
        print(f"Usuarios registrados: {users_count}")
        print(f"Parroquias registradas: {parroquias_count}")
        print(f"Bienes registrados: {inventarios_count}")
        
        if users_count == 0:
            print("No hay usuarios registrados. Ejecuta 'python populate_db.py' para crear datos iniciales.")
        
        if parroquias_count == 0:
            print("No hay parroquias registradas. Ejecuta 'python populate_db.py' para crear datos iniciales.")
        
        return True
        
    except Exception as e:
        print(f"Error conectando a MongoDB: {e}")
        print("\nSoluciones posibles:")
        print("1. Verificar que MongoDB este instalado")
        print("2. Iniciar el servicio de MongoDB:")
        print("   - Windows: net start MongoDB")
        print("   - Linux/Mac: sudo systemctl start mongod")
        print("3. Verificar que MongoDB este ejecutandose en puerto 27017")
        print("4. Instalar MongoDB Community Edition si no esta instalado")
        return False

def check_dependencies():
    """Verificar dependencias de Python"""
    try:
        import flask
        import flask_login
        import pymongo
        import werkzeug
        print("Todas las dependencias estan instaladas")
        return True
    except ImportError as e:
        print(f"Dependencia faltante: {e}")
        print("Instalar con: pip install flask flask-login pymongo werkzeug")
        return False

if __name__ == "__main__":
    print("Verificacion del Sistema de Inventario CONA\n")
    
    # Verificar dependencias
    deps_ok = check_dependencies()
    print()
    
    # Verificar MongoDB
    mongo_ok = test_mongodb_connection()
    print()
    
    if deps_ok and mongo_ok:
        print("Sistema listo para ejecutar!")
        print("Ejecuta: python app.py")
    else:
        print("Hay problemas que resolver antes de ejecutar el sistema")
        sys.exit(1)