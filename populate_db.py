from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['inventario_cona']

# Colecciones
users = db.users
parroquias = db.parroquias
inventarios = db.inventarios

def populate_parroquias():
    """Poblar con las 61 parroquias de ejemplo"""
    
    # Limpiar colección existente
    parroquias.delete_many({})
    
    parroquias_data = [
        # Provincia de Pichincha
        {'nombre': 'Quito', 'canton': 'Quito', 'codigo': 'QUI001'},
        {'nombre': 'Calderón', 'canton': 'Quito', 'codigo': 'CAL002'},
        {'nombre': 'Conocoto', 'canton': 'Quito', 'codigo': 'CON003'},
        {'nombre': 'Cumbayá', 'canton': 'Quito', 'codigo': 'CUM004'},
        {'nombre': 'Tumbaco', 'canton': 'Quito', 'codigo': 'TUM005'},
        {'nombre': 'Puembo', 'canton': 'Quito', 'codigo': 'PUE006'},
        {'nombre': 'Pifo', 'canton': 'Quito', 'codigo': 'PIF007'},
        {'nombre': 'Yaruquí', 'canton': 'Quito', 'codigo': 'YAR008'},
        {'nombre': 'Checa', 'canton': 'Quito', 'codigo': 'CHE009'},
        {'nombre': 'El Quinche', 'canton': 'Quito', 'codigo': 'QUI010'},
        
        # Provincia de Guayas
        {'nombre': 'Guayaquil', 'canton': 'Guayaquil', 'codigo': 'GUA011'},
        {'nombre': 'Pascuales', 'canton': 'Guayaquil', 'codigo': 'PAS012'},
        {'nombre': 'Tarqui', 'canton': 'Guayaquil', 'codigo': 'TAR013'},
        {'nombre': 'Ximena', 'canton': 'Guayaquil', 'codigo': 'XIM014'},
        {'nombre': 'Febres Cordero', 'canton': 'Guayaquil', 'codigo': 'FEB015'},
        {'nombre': 'García Moreno', 'canton': 'Guayaquil', 'codigo': 'GAR016'},
        {'nombre': 'Letamendi', 'canton': 'Guayaquil', 'codigo': 'LET017'},
        {'nombre': 'Olmedo', 'canton': 'Guayaquil', 'codigo': 'OLM018'},
        {'nombre': 'Rocafuerte', 'canton': 'Guayaquil', 'codigo': 'ROC019'},
        {'nombre': 'Sucre', 'canton': 'Guayaquil', 'codigo': 'SUC020'},
        
        # Provincia de Azuay
        {'nombre': 'Cuenca', 'canton': 'Cuenca', 'codigo': 'CUE021'},
        {'nombre': 'Baños', 'canton': 'Cuenca', 'codigo': 'BAN022'},
        {'nombre': 'Cumbe', 'canton': 'Cuenca', 'codigo': 'CUM023'},
        {'nombre': 'Chaucha', 'canton': 'Cuenca', 'codigo': 'CHA024'},
        {'nombre': 'Checa', 'canton': 'Cuenca', 'codigo': 'CHE025'},
        {'nombre': 'Chiquintad', 'canton': 'Cuenca', 'codigo': 'CHI026'},
        {'nombre': 'Llacao', 'canton': 'Cuenca', 'codigo': 'LLA027'},
        {'nombre': 'Molleturo', 'canton': 'Cuenca', 'codigo': 'MOL028'},
        {'nombre': 'Nulti', 'canton': 'Cuenca', 'codigo': 'NUL029'},
        {'nombre': 'Octavio Cordero', 'canton': 'Cuenca', 'codigo': 'OCT030'},
        
        # Provincia de Manabí
        {'nombre': 'Portoviejo', 'canton': 'Portoviejo', 'codigo': 'POR031'},
        {'nombre': 'Abdón Calderón', 'canton': 'Portoviejo', 'codigo': 'ABD032'},
        {'nombre': 'Alajuela', 'canton': 'Portoviejo', 'codigo': 'ALA033'},
        {'nombre': 'Colón', 'canton': 'Portoviejo', 'codigo': 'COL034'},
        {'nombre': 'Crucita', 'canton': 'Portoviejo', 'codigo': 'CRU035'},
        {'nombre': 'Picoazá', 'canton': 'Portoviejo', 'codigo': 'PIC036'},
        {'nombre': 'Pueblo Nuevo', 'canton': 'Portoviejo', 'codigo': 'PUE037'},
        {'nombre': 'Riochico', 'canton': 'Portoviejo', 'codigo': 'RIO038'},
        {'nombre': 'San Plácido', 'canton': 'Portoviejo', 'codigo': 'SAN039'},
        {'nombre': 'Simón Bolívar', 'canton': 'Portoviejo', 'codigo': 'SIM040'},
        
        # Provincia de El Oro
        {'nombre': 'Machala', 'canton': 'Machala', 'codigo': 'MAC041'},
        {'nombre': 'El Cambio', 'canton': 'Machala', 'codigo': 'CAM042'},
        {'nombre': 'Jambelí', 'canton': 'Machala', 'codigo': 'JAM043'},
        {'nombre': 'Jubones', 'canton': 'Machala', 'codigo': 'JUB044'},
        {'nombre': 'El Retiro', 'canton': 'Machala', 'codigo': 'RET045'},
        {'nombre': 'Puerto Bolívar', 'canton': 'Machala', 'codigo': 'PUE046'},
        
        # Provincia de Los Ríos
        {'nombre': 'Babahoyo', 'canton': 'Babahoyo', 'codigo': 'BAB047'},
        {'nombre': 'Caracol', 'canton': 'Babahoyo', 'codigo': 'CAR048'},
        {'nombre': 'Febres Cordero', 'canton': 'Babahoyo', 'codigo': 'FEB049'},
        {'nombre': 'Pimocha', 'canton': 'Babahoyo', 'codigo': 'PIM050'},
        {'nombre': 'Barreiro', 'canton': 'Babahoyo', 'codigo': 'BAR051'},
        
        # Provincia de Tungurahua
        {'nombre': 'Ambato', 'canton': 'Ambato', 'codigo': 'AMB052'},
        {'nombre': 'Atocha', 'canton': 'Ambato', 'codigo': 'ATO053'},
        {'nombre': 'Huachi Grande', 'canton': 'Ambato', 'codigo': 'HUA054'},
        {'nombre': 'Izamba', 'canton': 'Ambato', 'codigo': 'IZA055'},
        {'nombre': 'Juan Benigno Vela', 'canton': 'Ambato', 'codigo': 'JUA056'},
        {'nombre': 'La Merced', 'canton': 'Ambato', 'codigo': 'MER057'},
        {'nombre': 'La Península', 'canton': 'Ambato', 'codigo': 'PEN058'},
        {'nombre': 'Matriz', 'canton': 'Ambato', 'codigo': 'MAT059'},
        {'nombre': 'Pishilata', 'canton': 'Ambato', 'codigo': 'PIS060'},
        {'nombre': 'San Francisco', 'canton': 'Ambato', 'codigo': 'SAN061'}
    ]
    
    # Agregar fecha de creación a cada parroquia
    for parroquia in parroquias_data:
        parroquia['created_at'] = datetime.now()
    
    # Insertar parroquias
    result = parroquias.insert_many(parroquias_data)
    print(f"Se insertaron {len(result.inserted_ids)} parroquias")
    
    return list(parroquias.find())

def create_sample_users(parroquias_list):
    """Crear usuarios de ejemplo para algunas parroquias"""
    
    # Crear algunos administradores de parroquia
    admin_parroquias = [
        {
            'username': 'admin_quito',
            'password': generate_password_hash('admin123'),
            'role': 'admin_parroquia',
            'nombre': 'María',
            'apellido': 'González',
            'email': 'maria.gonzalez@quito.gob.ec',
            'parroquia_id': parroquias_list[0]['_id'],  # Quito
            'created_at': datetime.now()
        },
        {
            'username': 'admin_guayaquil',
            'password': generate_password_hash('admin123'),
            'role': 'admin_parroquia',
            'nombre': 'Carlos',
            'apellido': 'Rodríguez',
            'email': 'carlos.rodriguez@guayaquil.gob.ec',
            'parroquia_id': parroquias_list[10]['_id'],  # Guayaquil
            'created_at': datetime.now()
        },
        {
            'username': 'admin_cuenca',
            'password': generate_password_hash('admin123'),
            'role': 'admin_parroquia',
            'nombre': 'Ana',
            'apellido': 'Martínez',
            'email': 'ana.martinez@cuenca.gob.ec',
            'parroquia_id': parroquias_list[20]['_id'],  # Cuenca
            'created_at': datetime.now()
        }
    ]
    
    # Insertar usuarios
    users.insert_many(admin_parroquias)
    print(f"Se crearon {len(admin_parroquias)} administradores de parroquia")

def create_sample_inventory():
    """Crear inventario de ejemplo"""
    
    # Obtener algunas parroquias
    quito = parroquias.find_one({'codigo': 'QUI001'})
    guayaquil = parroquias.find_one({'codigo': 'GUA011'})
    
    bienes_ejemplo = [
        # Bienes para Quito
        {
            'codigo': 'COMP-QUI-001',
            'nombre': 'Computadora de Escritorio HP',
            'tipo': 'Computadora',
            'marca': 'HP',
            'modelo': 'EliteDesk 800 G6',
            'estado': 'disponible',
            'descripcion': 'Computadora de escritorio para uso administrativo',
            'parroquia_id': quito['_id'],
            'created_at': datetime.now()
        },
        {
            'codigo': 'IMP-QUI-001',
            'nombre': 'Impresora Multifuncional Canon',
            'tipo': 'Impresora',
            'marca': 'Canon',
            'modelo': 'PIXMA G3110',
            'estado': 'disponible',
            'descripcion': 'Impresora multifuncional con sistema de tinta continua',
            'parroquia_id': quito['_id'],
            'created_at': datetime.now()
        },
        {
            'codigo': 'MON-QUI-001',
            'nombre': 'Monitor LED Samsung',
            'tipo': 'Monitor',
            'marca': 'Samsung',
            'modelo': 'F24T450FQL',
            'estado': 'disponible',
            'descripcion': 'Monitor LED de 24 pulgadas Full HD',
            'parroquia_id': quito['_id'],
            'created_at': datetime.now()
        },
        
        # Bienes para Guayaquil
        {
            'codigo': 'COMP-GUA-001',
            'nombre': 'Laptop Dell Inspiron',
            'tipo': 'Computadora',
            'marca': 'Dell',
            'modelo': 'Inspiron 15 3000',
            'estado': 'disponible',
            'descripcion': 'Laptop para trabajo móvil',
            'parroquia_id': guayaquil['_id'],
            'created_at': datetime.now()
        },
        {
            'codigo': 'PROJ-GUA-001',
            'nombre': 'Proyector Epson',
            'tipo': 'Proyector',
            'marca': 'Epson',
            'modelo': 'PowerLite X41+',
            'estado': 'disponible',
            'descripcion': 'Proyector para presentaciones',
            'parroquia_id': guayaquil['_id'],
            'created_at': datetime.now()
        }
    ]
    
    inventarios.insert_many(bienes_ejemplo)
    print(f"Se crearon {len(bienes_ejemplo)} bienes de ejemplo")

def main():
    print("Iniciando poblacion de la base de datos...")
    
    # Crear usuario super admin si no existe
    if not users.find_one({'username': 'admin'}):
        admin_user = {
            'username': 'admin',
            'password': generate_password_hash('admin123'),
            'role': 'super_admin',
            'nombre': 'Administrador',
            'apellido': 'Principal',
            'email': 'admin@cona.gov.ec',
            'parroquia_id': None,
            'created_at': datetime.now()
        }
        users.insert_one(admin_user)
        print("Usuario super admin creado")
    
    # Poblar parroquias
    parroquias_list = populate_parroquias()
    
    # Crear usuarios de ejemplo
    create_sample_users(parroquias_list)
    
    # Crear inventario de ejemplo
    create_sample_inventory()
    
    print("\nBase de datos poblada exitosamente!")
    print("\nCredenciales de acceso:")
    print("Super Admin: admin / admin123")
    print("Admin Quito: admin_quito / admin123")
    print("Admin Guayaquil: admin_guayaquil / admin123")
    print("Admin Cuenca: admin_cuenca / admin123")
    print("Técnico Quito: tecnico1_quito / tecnico123")
    print("Técnico Guayaquil: tecnico1_guayaquil / tecnico123")

if __name__ == "__main__":
    main()