#!/usr/bin/env python3
"""
Script para inicializar datos de prueba del sistema
"""

from pymongo import MongoClient
import bcrypt
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from config import MONGO_URI
import random

def init_sample_data():
    client = MongoClient(MONGO_URI)
    cona_inv = client['cona_inv']
    users = cona_inv['users']
    parroquias = cona_inv['parroquias']
    inventarios = cona_inv['inventarios']
    bienes_asignados = cona_inv['bienes_asignados']
    audit_logs = cona_inv['audit_logs']
    
    print("Inicializando datos de prueba...")
    
    # Obtener algunas parroquias
    parroquias_list = list(parroquias.find().limit(5))
    
    if not parroquias_list:
        print("No hay parroquias. Ejecuta cargar_parroquias.py primero")
        return
    
    # Crear bienes de ejemplo
    tipos_equipos = ['Computadora', 'Laptop', 'Impresora', 'Monitor', 'Proyector', 'Scanner']
    marcas = ['HP', 'Dell', 'Lenovo', 'Canon', 'Epson', 'Samsung']
    estados_equipo = ['En funcionamiento', 'Dar mantenimiento', 'Nuevo', 'En reparación']
    colores = ['Negro', 'Blanco', 'Gris', 'Plateado']
    
    bienes_creados = 0
    for parroquia in parroquias_list:
        for i in range(random.randint(5, 15)):
            tipo = random.choice(tipos_equipos)
            marca = random.choice(marcas)
            
            bien_data = {
                'codigo': f"{parroquia['codigo']}-{tipo[:3].upper()}-{i+1:03d}",
                'nombre': f"{tipo} {marca} {i+1}",
                'tipo': tipo,
                'marca': marca,
                'modelo': f"Modelo-{random.randint(1000, 9999)}",
                'color': random.choice(colores),
                'estado': random.choice(['disponible', 'asignado', 'en_mantenimiento']),
                'estado_equipo': random.choice(estados_equipo),
                'descripcion': f"Equipo {tipo} para uso administrativo",
                'parroquia_id': parroquia['_id'],
                'created_at': datetime.now() - timedelta(days=random.randint(1, 365))
            }
            
            # Verificar si ya existe
            if not inventarios.find_one({'codigo': bien_data['codigo']}):
                inventarios.insert_one(bien_data)
                bienes_creados += 1
    
    print(f"Bienes de ejemplo creados: {bienes_creados}")
    
    # Crear algunas asignaciones de ejemplo
    bienes_disponibles = list(inventarios.find({'estado': 'asignado'}))
    tecnicos = list(users.find({'role': 'tecnico'}))
    
    asignaciones_creadas = 0
    for bien in bienes_disponibles[:10]:  # Solo primeros 10
        if tecnicos:
            tecnico = random.choice(tecnicos)
            asignacion = {
                'bien_id': bien['_id'],
                'responsable': f"{tecnico['nombre']} {tecnico['apellido']}",
                'parroquia_id': bien['parroquia_id'],
                'fecha_asignacion': datetime.now() - timedelta(days=random.randint(1, 180)),
                'observaciones': 'Asignación de prueba',
                'estado': 'activo'
            }
            
            if not bienes_asignados.find_one({'bien_id': bien['_id'], 'estado': 'activo'}):
                bienes_asignados.insert_one(asignacion)
                asignaciones_creadas += 1
    
    print(f"Asignaciones de ejemplo creadas: {asignaciones_creadas}")
    
    # Crear logs de auditoría de ejemplo
    acciones = ['LOGIN', 'CREATE_ASSET', 'ASSIGN_ASSET', 'CREATE_USER']
    usuarios_ejemplo = ['admin', 'admin_par01', 'tecnico_quito']
    
    logs_creados = 0
    for i in range(50):
        log_entry = {
            'action': random.choice(acciones),
            'details': f'Acción de prueba #{i+1}',
            'user_id': random.choice(usuarios_ejemplo),
            'timestamp': datetime.now() - timedelta(hours=random.randint(1, 720)),
            'ip_address': f"192.168.1.{random.randint(1, 254)}"
        }
        audit_logs.insert_one(log_entry)
        logs_creados += 1
    
    print(f"Logs de auditoría creados: {logs_creados}")
    print("\nDatos de prueba inicializados exitosamente!")

if __name__ == '__main__':
    init_sample_data()