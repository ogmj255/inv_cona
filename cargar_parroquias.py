from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI

# Conexión a MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client['cona_inv']
parroquias_collection = db['parroquias']

# Lista de parroquias
parroquias = [
    {"nombre": "EL CARMEN DE PIJILI", "canton": "CAMILO PONCE ENRIQUE"},
    {"nombre": "LA UNIÓN", "canton": "CHORDELEG"},
    {"nombre": "LUIS GALARZA O (DELEGSOL)", "canton": "CHORDELEG"},
    {"nombre": "PRINCIPAL", "canton": "CHORDELEG"},
    {"nombre": "SAN MARTIN DE PUZHIO", "canton": "CHORDELEG"},
    {"nombre": "BAÑOS", "canton": "CUENCA"},
    {"nombre": "CHAUCHA / ANGAS", "canton": "CUENCA"},
    {"nombre": "CHECA JIDCAY", "canton": "CUENCA"},
    {"nombre": "CHIQUINTAD", "canton": "CUENCA"},
    {"nombre": "CUMBE", "canton": "CUENCA"},
    {"nombre": "EL VALLE", "canton": "CUENCA"},
    {"nombre": "LLACAO", "canton": "CUENCA"},
    {"nombre": "MOLLETURO", "canton": "CUENCA"},
    {"nombre": "NULTI / MULTI", "canton": "CUENCA"},
    {"nombre": "OCTAVIO CORDERO PALACIOS", "canton": "CUENCA"},
    {"nombre": "PACCHA", "canton": "CUENCA"},
    {"nombre": "QUINGEO", "canton": "CUENCA"},
    {"nombre": "RICAURTE", "canton": "CUENCA"},
    {"nombre": "SAN JOAQUÍN", "canton": "CUENCA"},
    {"nombre": "SANTA ANA", "canton": "CUENCA"},
    {"nombre": "SAYAUSI", "canton": "CUENCA"},
    {"nombre": "SIDCAY", "canton": "CUENCA"},
    {"nombre": "SININCAY", "canton": "CUENCA"},
    {"nombre": "TARQUI", "canton": "CUENCA"},
    {"nombre": "TURI", "canton": "CUENCA"},
    {"nombre": "VICTORIA DEL PORTETE", "canton": "CUENCA"},
    {"nombre": "SAN VICENTE", "canton": "EL PAN"},
    {"nombre": "LA ASUNCIÓN", "canton": "GIRÓN"},
    {"nombre": "SAN GERARDO", "canton": "GIRÓN"},
    {"nombre": "DANIEL CORDOVA TORAL", "canton": "GUALACEO"},
    {"nombre": "JADÁN", "canton": "GUALACEO"},
    {"nombre": "LUIS CORDERO VEGA", "canton": "GUALACEO"},
    {"nombre": "MARIANO MORENO / CALLASAY", "canton": "GUALACEO"},
    {"nombre": "REMIGIO CRESPO TORAL", "canton": "GUALACEO"},
    {"nombre": "SAN JUAN", "canton": "GUALACEO"},
    {"nombre": "SIMÓN BOLIVAR", "canton": "GUALACEO"},
    {"nombre": "ZHIDMAD", "canton": "GUALACEO"},
    {"nombre": "COCHAPATA", "canton": "NABÓN"},
    {"nombre": "EL PROGRESO", "canton": "NABÓN"},
    {"nombre": "LAS NIEVES", "canton": "NABÓN"},
    {"nombre": "SUSUDEL", "canton": "OÑA"},
    {"nombre": "BULAN / J. VICTOR IZQUIERDO", "canton": "PAUTE"},
    {"nombre": "CHICAN / GUILLERMO ORTEGA", "canton": "PAUTE"},
    {"nombre": "DUG-DUG", "canton": "PAUTE"},
    {"nombre": "EL CABO", "canton": "PAUTE"},
    {"nombre": "GUARAINAG", "canton": "PAUTE"},
    {"nombre": "SAN CRISTOBAL", "canton": "PAUTE"},
    {"nombre": "TOMEBAMBA", "canton": "PAUTE"},
    {"nombre": "SAN RAFAEL DE SHARUG", "canton": "PUCARÁ"},
    {"nombre": "CHUMBLÍN", "canton": "SAN FERNANDO"},
    {"nombre": "ABDON CALDERÓN / LA UNIÓN", "canton": "SANTA ISABEL"},
    {"nombre": "SAN SALVADOR DE CAÑARIBAMBA", "canton": "SANTA ISABEL"},
    {"nombre": "SHAGLI", "canton": "SANTA ISABEL"},
    {"nombre": "AMALUZA", "canton": "SEVILLA DE ORO"},
    {"nombre": "PALMAS", "canton": "SEVILLA DE ORO"},
    {"nombre": "CUTCHIL", "canton": "SIGSIG"},
    {"nombre": "GUEL", "canton": "SIGSIG"},
    {"nombre": "JIMA", "canton": "SIGSIG"},
    {"nombre": "LUDO", "canton": "SIGSIG"},
    {"nombre": "SAN BARTOLOMÉ", "canton": "SIGSIG"},
    {"nombre": "SAN JOSÉ DE RARANGA", "canton": "SIGSIG"}
]

# Limpiar colección existente
parroquias_collection.delete_many({})

# Insertar parroquias con códigos únicos
for i, parroquia in enumerate(parroquias, 1):
    parroquia_doc = {
        "nombre": parroquia["nombre"],
        "canton": parroquia["canton"],
        "codigo": f"PAR{i:03d}",
        "created_at": datetime.now()
    }
    parroquias_collection.insert_one(parroquia_doc)

print(f"Se han cargado {len(parroquias)} parroquias en la base de datos.")
print("Proceso completado exitosamente.")