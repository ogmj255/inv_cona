from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

# Conectar a MongoDB
client = MongoClient(MONGO_URI)
db = client['cona_inv']
parroquias = db.parroquias

def add_parroquias():
    # Verificar si ya existen parroquias
    if parroquias.count_documents({}) > 0:
        print(f"Ya existen {parroquias.count_documents({})} parroquias en la base de datos")
        return
    
    # Lista de parroquias de Ecuador
    parroquias_data = [
        # Pichincha
        {'nombre': 'Quito', 'canton': 'Quito', 'codigo': 'QUI001', 'provincia': 'Pichincha'},
        {'nombre': 'Calderón', 'canton': 'Quito', 'codigo': 'CAL002', 'provincia': 'Pichincha'},
        {'nombre': 'Conocoto', 'canton': 'Quito', 'codigo': 'CON003', 'provincia': 'Pichincha'},
        {'nombre': 'Cumbayá', 'canton': 'Quito', 'codigo': 'CUM004', 'provincia': 'Pichincha'},
        {'nombre': 'Tumbaco', 'canton': 'Quito', 'codigo': 'TUM005', 'provincia': 'Pichincha'},
        
        # Guayas
        {'nombre': 'Guayaquil', 'canton': 'Guayaquil', 'codigo': 'GUA006', 'provincia': 'Guayas'},
        {'nombre': 'Pascuales', 'canton': 'Guayaquil', 'codigo': 'PAS007', 'provincia': 'Guayas'},
        {'nombre': 'Tarqui', 'canton': 'Guayaquil', 'codigo': 'TAR008', 'provincia': 'Guayas'},
        {'nombre': 'Ximena', 'canton': 'Guayaquil', 'codigo': 'XIM009', 'provincia': 'Guayas'},
        {'nombre': 'Febres Cordero', 'canton': 'Guayaquil', 'codigo': 'FEB010', 'provincia': 'Guayas'},
        
        # Azuay
        {'nombre': 'Cuenca', 'canton': 'Cuenca', 'codigo': 'CUE011', 'provincia': 'Azuay'},
        {'nombre': 'Baños', 'canton': 'Cuenca', 'codigo': 'BAN012', 'provincia': 'Azuay'},
        {'nombre': 'Cumbe', 'canton': 'Cuenca', 'codigo': 'CUM013', 'provincia': 'Azuay'},
        {'nombre': 'Chaucha', 'canton': 'Cuenca', 'codigo': 'CHA014', 'provincia': 'Azuay'},
        {'nombre': 'Checa', 'canton': 'Cuenca', 'codigo': 'CHE015', 'provincia': 'Azuay'},
        
        # Manabí
        {'nombre': 'Portoviejo', 'canton': 'Portoviejo', 'codigo': 'POR016', 'provincia': 'Manabí'},
        {'nombre': 'Abdón Calderón', 'canton': 'Portoviejo', 'codigo': 'ABD017', 'provincia': 'Manabí'},
        {'nombre': 'Alajuela', 'canton': 'Portoviejo', 'codigo': 'ALA018', 'provincia': 'Manabí'},
        {'nombre': 'Colón', 'canton': 'Portoviejo', 'codigo': 'COL019', 'provincia': 'Manabí'},
        {'nombre': 'Crucita', 'canton': 'Portoviejo', 'codigo': 'CRU020', 'provincia': 'Manabí'},
        
        # El Oro
        {'nombre': 'Machala', 'canton': 'Machala', 'codigo': 'MAC021', 'provincia': 'El Oro'},
        {'nombre': 'El Cambio', 'canton': 'Machala', 'codigo': 'CAM022', 'provincia': 'El Oro'},
        {'nombre': 'Jambelí', 'canton': 'Machala', 'codigo': 'JAM023', 'provincia': 'El Oro'},
        {'nombre': 'Jubones', 'canton': 'Machala', 'codigo': 'JUB024', 'provincia': 'El Oro'},
        {'nombre': 'El Retiro', 'canton': 'Machala', 'codigo': 'RET025', 'provincia': 'El Oro'},
        
        # Los Ríos
        {'nombre': 'Babahoyo', 'canton': 'Babahoyo', 'codigo': 'BAB026', 'provincia': 'Los Ríos'},
        {'nombre': 'Caracol', 'canton': 'Babahoyo', 'codigo': 'CAR027', 'provincia': 'Los Ríos'},
        {'nombre': 'Febres Cordero', 'canton': 'Babahoyo', 'codigo': 'FEB028', 'provincia': 'Los Ríos'},
        {'nombre': 'Pimocha', 'canton': 'Babahoyo', 'codigo': 'PIM029', 'provincia': 'Los Ríos'},
        {'nombre': 'Barreiro', 'canton': 'Babahoyo', 'codigo': 'BAR030', 'provincia': 'Los Ríos'},
        
        # Tungurahua
        {'nombre': 'Ambato', 'canton': 'Ambato', 'codigo': 'AMB031', 'provincia': 'Tungurahua'},
        {'nombre': 'Atocha', 'canton': 'Ambato', 'codigo': 'ATO032', 'provincia': 'Tungurahua'},
        {'nombre': 'Huachi Grande', 'canton': 'Ambato', 'codigo': 'HUA033', 'provincia': 'Tungurahua'},
        {'nombre': 'Izamba', 'canton': 'Ambato', 'codigo': 'IZA034', 'provincia': 'Tungurahua'},
        {'nombre': 'Juan Benigno Vela', 'canton': 'Ambato', 'codigo': 'JUA035', 'provincia': 'Tungurahua'},
        
        # Loja
        {'nombre': 'Loja', 'canton': 'Loja', 'codigo': 'LOJ036', 'provincia': 'Loja'},
        {'nombre': 'El Valle', 'canton': 'Loja', 'codigo': 'VAL037', 'provincia': 'Loja'},
        {'nombre': 'Sucre', 'canton': 'Loja', 'codigo': 'SUC038', 'provincia': 'Loja'},
        {'nombre': 'San Sebastián', 'canton': 'Loja', 'codigo': 'SAN039', 'provincia': 'Loja'},
        {'nombre': 'Malacatos', 'canton': 'Loja', 'codigo': 'MAL040', 'provincia': 'Loja'},
        
        # Imbabura
        {'nombre': 'Ibarra', 'canton': 'Ibarra', 'codigo': 'IBA041', 'provincia': 'Imbabura'},
        {'nombre': 'Alpachaca', 'canton': 'Ibarra', 'codigo': 'ALP042', 'provincia': 'Imbabura'},
        {'nombre': 'Caranqui', 'canton': 'Ibarra', 'codigo': 'CAR043', 'provincia': 'Imbabura'},
        {'nombre': 'Priorato', 'canton': 'Ibarra', 'codigo': 'PRI044', 'provincia': 'Imbabura'},
        {'nombre': 'San Francisco', 'canton': 'Ibarra', 'codigo': 'SAN045', 'provincia': 'Imbabura'},
        
        # Chimborazo
        {'nombre': 'Riobamba', 'canton': 'Riobamba', 'codigo': 'RIO046', 'provincia': 'Chimborazo'},
        {'nombre': 'Lizarzaburu', 'canton': 'Riobamba', 'codigo': 'LIZ047', 'provincia': 'Chimborazo'},
        {'nombre': 'Maldonado', 'canton': 'Riobamba', 'codigo': 'MAL048', 'provincia': 'Chimborazo'},
        {'nombre': 'Veloz', 'canton': 'Riobamba', 'codigo': 'VEL049', 'provincia': 'Chimborazo'},
        {'nombre': 'Velasco', 'canton': 'Riobamba', 'codigo': 'VEL050', 'provincia': 'Chimborazo'},
        
        # Cotopaxi
        {'nombre': 'Latacunga', 'canton': 'Latacunga', 'codigo': 'LAT051', 'provincia': 'Cotopaxi'},
        {'nombre': 'Eloy Alfaro', 'canton': 'Latacunga', 'codigo': 'ELO052', 'provincia': 'Cotopaxi'},
        {'nombre': 'Ignacio Flores', 'canton': 'Latacunga', 'codigo': 'IGN053', 'provincia': 'Cotopaxi'},
        {'nombre': 'Juan Montalvo', 'canton': 'Latacunga', 'codigo': 'JUA054', 'provincia': 'Cotopaxi'},
        {'nombre': 'La Matriz', 'canton': 'Latacunga', 'codigo': 'MAT055', 'provincia': 'Cotopaxi'},
        
        # Esmeraldas
        {'nombre': 'Esmeraldas', 'canton': 'Esmeraldas', 'codigo': 'ESM056', 'provincia': 'Esmeraldas'},
        {'nombre': 'Bartolomé Ruiz', 'canton': 'Esmeraldas', 'codigo': 'BAR057', 'provincia': 'Esmeraldas'},
        {'nombre': '5 de Agosto', 'canton': 'Esmeraldas', 'codigo': 'AGO058', 'provincia': 'Esmeraldas'},
        {'nombre': 'Luis Tello', 'canton': 'Esmeraldas', 'codigo': 'LUI059', 'provincia': 'Esmeraldas'},
        {'nombre': 'Simón Plata Torres', 'canton': 'Esmeraldas', 'codigo': 'SIM060', 'provincia': 'Esmeraldas'},
        
        # Santo Domingo
        {'nombre': 'Santo Domingo', 'canton': 'Santo Domingo', 'codigo': 'STO061', 'provincia': 'Santo Domingo de los Tsáchilas'}
    ]
    
    # Agregar fecha de creación
    for parroquia in parroquias_data:
        parroquia['created_at'] = datetime.now()
    
    # Insertar parroquias
    result = parroquias.insert_many(parroquias_data)
    print(f"Se insertaron {len(result.inserted_ids)} parroquias")

if __name__ == "__main__":
    add_parroquias()
    print("Parroquias agregadas exitosamente!")