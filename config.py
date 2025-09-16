import os

# MongoDB URI - usar variable de entorno o valor por defecto
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/cona_inv')

# Para debugging en producción
if 'RENDER' in os.environ:
    print(f"MongoDB URI configurado: {MONGO_URI[:20]}..." if len(MONGO_URI) > 20 else MONGO_URI)